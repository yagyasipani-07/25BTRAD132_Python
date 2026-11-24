#!/usr/bin/env python3
"""
hwsnap - Hardware snapshot and cryptographic auditing module for HWGuard.
Captures hardware serials and IDs across macOS, Linux, and Windows.
"""
import hashlib
import json
import os
import platform
import re
import subprocess

MAX_CYCLE_DELTA = 50


def keccak256(data: bytes) -> str:
    """Return 0x-prefixed SHA3-256 / Keccak-256 hash."""
    return "0x" + hashlib.sha3_256(data).hexdigest()


def build_components(raw, salt: str):
    """
    Given raw = [(type, slot, value), ...] and salt (hex str),
    returns a list of component dicts with salted hashes.
    """
    comps = []
    for t, s, v in raw:
        payload = f"{salt}:{t}:{s}:{v}".encode("utf-8")
        comps.append({
            "type": t,
            "slot": s,
            "hash": keccak256(payload)
        })
    return comps


def snapshot_root(comps) -> str:
    """Compute Merkle-style root hash over sorted component hashes."""
    sorted_comps = sorted(comps, key=lambda x: (x["type"], x["slot"]))
    joined = "".join(c["hash"] for c in sorted_comps)
    return keccak256(joined.encode("utf-8"))


def _collect_macos():
    raw = []
    cycles = None
    skipped = []

    # Logic Board Serial & Hardware UUID
    try:
        out = subprocess.check_output(["ioreg", "-d2", "-c", "IOPlatformExpertDevice"]).decode("utf-8", errors="ignore")
        ser_match = re.search(r'"IOPlatformSerialNumber"\s*=\s*"([^"]+)"', out)
        uuid_match = re.search(r'"IOPlatformUUID"\s*=\s*"([^"]+)"', out)
        if ser_match:
            raw.append(("Logic Board", "Serial", ser_match.group(1).strip()))
        if uuid_match:
            raw.append(("Logic Board", "UUID", uuid_match.group(1).strip()))
    except Exception as e:
        skipped.append(f"Logic Board ({e})")

    # CPU / Processor Model
    try:
        model = subprocess.check_output(["sysctl", "-n", "hw.model"]).decode("utf-8", errors="ignore").strip()
        cpu_name = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode("utf-8", errors="ignore").strip()
        raw.append(("CPU", "Processor", cpu_name or model))
        if model:
            raw.append(("System", "Model", model))
    except Exception:
        try:
            model = subprocess.check_output(["sysctl", "-n", "hw.model"]).decode("utf-8", errors="ignore").strip()
            raw.append(("System", "Model", model))
        except Exception as e:
            skipped.append(f"CPU ({e})")

    # Physical Memory (RAM)
    try:
        mem_bytes = int(subprocess.check_output(["sysctl", "-n", "hw.memsize"]).decode("utf-8", errors="ignore").strip())
        mem_gb = f"{mem_bytes / (1024**3):.1f} GB"
        raw.append(("RAM", "Bank 0", mem_gb))
    except Exception as e:
        skipped.append(f"RAM ({e})")

    # Storage Disk 0
    try:
        disk_info = subprocess.check_output(["diskutil", "info", "disk0"]).decode("utf-8", errors="ignore")
        name_match = re.search(r'Device / Media Name:\s*(.+)', disk_info)
        uuid_match = re.search(r'(?:Disk / Partition UUID|Volume UUID):\s*([A-Fa-f0-9-]+)', disk_info)
        if name_match:
            raw.append(("Storage", "disk0 Media", name_match.group(1).strip()))
        if uuid_match:
            raw.append(("Storage", "disk0 UUID", uuid_match.group(1).strip()))
    except Exception as e:
        skipped.append(f"Storage ({e})")

    # Battery Cycle Count & Serial
    try:
        batt_info = subprocess.check_output(["ioreg", "-r", "-c", "AppleSmartBattery"]).decode("utf-8", errors="ignore")
        cyc_match = re.search(r'"CycleCount"\s*=\s*(\d+)', batt_info)
        if cyc_match:
            cycles = int(cyc_match.group(1))
            raw.append(("Battery", "Cycle Count", str(cycles)))
        ser_match = re.search(r'"Serial"\s*=\s*"([^"]+)"', batt_info)
        if ser_match:
            raw.append(("Battery", "Serial", ser_match.group(1).strip()))
    except Exception:
        # Not all devices (e.g. desktop Mac / Mac mini) have a battery
        pass

    return raw, cycles, skipped


def _collect_linux():
    raw = []
    cycles = None
    skipped = []

    def read_sysfs(path):
        try:
            with open(path, "r") as f:
                return f.read().strip()
        except Exception:
            return None

    # DMI board serial
    board_ser = read_sysfs("/sys/class/dmi/id/board_serial") or read_sysfs("/sys/class/dmi/id/product_serial")
    if board_ser:
        raw.append(("Logic Board", "Serial", board_ser))
    product_uuid = read_sysfs("/sys/class/dmi/id/product_uuid")
    if product_uuid:
        raw.append(("Logic Board", "UUID", product_uuid))

    # CPU
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    raw.append(("CPU", "Processor", line.split(":", 1)[1].strip()))
                    break
    except Exception as e:
        skipped.append(f"CPU ({e})")

    # RAM
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if "MemTotal" in line:
                    raw.append(("RAM", "Total", line.split(":", 1)[1].strip()))
                    break
    except Exception as e:
        skipped.append(f"RAM ({e})")

    # Battery
    batt_cycle = read_sysfs("/sys/class/power_supply/BAT0/cycle_count")
    if batt_cycle and batt_cycle.isdigit():
        cycles = int(batt_cycle)
        raw.append(("Battery", "Cycle Count", str(cycles)))

    return raw, cycles, skipped


def _collect_windows():
    raw = []
    cycles = None
    skipped = []

    try:
        out = subprocess.check_output(["wmic", "baseboard", "get", "SerialNumber"], shell=True).decode()
        lines = [l.strip() for l in out.splitlines() if l.strip() and "SerialNumber" not in l]
        if lines:
            raw.append(("Logic Board", "Serial", lines[0]))
    except Exception as e:
        skipped.append(f"Logic Board ({e})")

    try:
        out = subprocess.check_output(["wmic", "cpu", "get", "Name"], shell=True).decode()
        lines = [l.strip() for l in out.splitlines() if l.strip() and "Name" not in l]
        if lines:
            raw.append(("CPU", "Processor", lines[0]))
    except Exception as e:
        skipped.append(f"CPU ({e})")

    return raw, cycles, skipped


def collect():
    """Collect hardware data for the current platform."""
    sys_name = platform.system()
    if sys_name == "Darwin":
        return _collect_macos()
    elif sys_name == "Linux":
        return _collect_linux()
    elif sys_name == "Windows":
        return _collect_windows()
    else:
        return [("System", "OS", sys_name)], None, []
