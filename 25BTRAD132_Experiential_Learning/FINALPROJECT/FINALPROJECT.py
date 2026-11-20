#!/usr/bin/env python3
"""
HWGuard - portable hardware integrity tool (runs from a pendrive)

First run  : Scan device -> user reviews every component -> sets password -> saved
Later runs : [Verify device]  (no password)
             [Update device configuration]  (password required)

State lives next to the exe in ./hwguard_data/state.json as an append-only,
hash-chained config log. The head hash of that log is what you anchor on-chain.
Only salted keccak256 hashes are stored, never raw serials.

Needs hwsnap.py in the same folder (build step bundles it).
Build:  pyinstaller --onefile --windowed --uac-admin --name HWGuard hwguard.py
"""
import hashlib, hmac, json, os, platform, secrets, subprocess, sys, threading, time
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

# no flashing console windows when the exe is built --windowed
if platform.system() == "Windows":
    _orig_run = subprocess.run
    subprocess.run = lambda *a, **k: _orig_run(*a, creationflags=0x08000000, **k)

import hwsnap as hs  # noqa: E402


# ---------------- storage ----------------
def base_dir() -> Path:
    return Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent


STATE_FILE = base_dir() / "hwguard_data" / "state.json"


def load_state():
    try:
        return json.loads(STATE_FILE.read_text())
    except FileNotFoundError:
        return None


def save_state(st):
    STATE_FILE.parent.mkdir(exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(st, indent=2))
    os.replace(tmp, STATE_FILE)


# ---------------- crypto ----------------
def derive_key(pw: str, salt_hex: str) -> bytes:
    return hashlib.scrypt(pw.encode(), salt=bytes.fromhex(salt_hex), n=2 ** 15, r=8, p=1,
                          maxmem=2 ** 26, dklen=32)


def pw_tag(key: bytes) -> str:
    return hmac.new(key, b"hwguard-pw", hashlib.sha256).hexdigest()


def entry_hash(body: dict) -> str:
    return hs.keccak256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode())


def make_entry(seq, salt, raw, cycles, prev, key, note):
    comps = hs.build_components(raw, salt)
    body = {"seq": seq, "timestamp": int(time.time()), "note": note, "components": comps,
            "battery_cycles": cycles, "root": hs.snapshot_root(comps), "prev": prev}
    h = entry_hash(body)
    mac = hmac.new(key, bytes.fromhex(h[2:]), hashlib.sha256).hexdigest()
    return {**body, "hash": h, "mac": mac}


def chain_ok(st) -> bool:
    prev = "0x" + "00" * 32
    for e in st["log"]:
        body = {k: v for k, v in e.items() if k not in ("hash", "mac")}
        if body["prev"] != prev or entry_hash(body) != e["hash"]:
            return False
        prev = e["hash"]
    return True


def compare(entry, raw, cycles, salt):
    """returns (rows, notes). rows = (type, slot, status, raw_serial)"""
    new = {(c["type"], c["slot"]): c["hash"] for c in hs.build_components(raw, salt)}
    old = {(c["type"], c["slot"]): c["hash"] for c in entry["components"]}
    rawmap = {(t, s): v for t, s, v in raw}
    rows = []
    for k, h in old.items():
        status = "MISSING" if k not in new else ("OK" if new[k] == h else "MISMATCH")
        rows.append((k[0], k[1], status, rawmap.get(k, "")))
    for k in sorted(new.keys() - old.keys()):
        rows.append((k[0], k[1], "NEW", rawmap[k]))
    notes = []
    oc = entry.get("battery_cycles")
    if oc is not None and cycles is not None:
        if cycles < oc:
            notes.append(f"Battery cycles went DOWN ({oc} -> {cycles}): counter rollback")
        elif cycles - oc > hs.MAX_CYCLE_DELTA:
            notes.append(f"Battery cycles jumped {oc} -> {cycles}: heavy use while in repair")
    return rows, notes


# ---------------- GUI ----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HWGuard")
        self.geometry("820x560")
        self.st = load_state()
        self.body = ttk.Frame(self, padding=14)
        self.body.pack(fill="both", expand=True)
        self.show_home()

    # -- helpers --
    def clear(self):
        for w in self.body.winfo_children():
            w.destroy()

    def title_label(self, text, sub=None):
        ttk.Label(self.body, text=text, font=("Segoe UI", 16, "bold")).pack(anchor="w")
        if sub:
            ttk.Label(self.body, text=sub, wraplength=760, foreground="#555").pack(anchor="w", pady=(2, 10))

    def tree(self, cols, rows, widths):
        frame = ttk.Frame(self.body)
        frame.pack(fill="both", expand=True, pady=6)
        t = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        for c, w in zip(cols, widths):
            t.heading(c, text=c)
            t.column(c, width=w, anchor="w")
        t.tag_configure("ok", foreground="#1a7f37")
        t.tag_configure("bad", foreground="#c62828")
        t.tag_configure("new", foreground="#b26a00")
        sb = ttk.Scrollbar(frame, orient="vertical", command=t.yview)
        t.configure(yscrollcommand=sb.set)
        t.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        for r in rows:
            tag = ()
            if len(r) > 2 and r[2] in ("OK", "MISMATCH", "MISSING", "NEW"):
                tag = ("ok",) if r[2] == "OK" else ("new",) if r[2] == "NEW" else ("bad",)
            t.insert("", "end", values=r, tags=tag)
        return t

    def busy(self, msg, work, done):
        self.clear()
        self.title_label(msg, "Reading hardware, this takes a few seconds...")
        pb = ttk.Progressbar(self.body, mode="indeterminate")
        pb.pack(fill="x", pady=20)
        pb.start(12)

        def run():
            try:
                res = work()
            except BaseException as e:  # incl. SystemExit from unsupported OS
                res = e
            self.after(0, lambda: done(res))

        threading.Thread(target=run, daemon=True).start()

    def scan_failed(self, res):
        messagebox.showerror("Scan failed", str(res) or "Unknown error")
        self.show_home()

    def buttons(self, *items):
        bar = ttk.Frame(self.body)
        bar.pack(fill="x", pady=(10, 0))
        for text, cmd in items:
            ttk.Button(bar, text=text, command=cmd).pack(side="left", padx=(0, 8))

    # -- screens --
    def show_home(self):
        self.clear()
        if self.st is None:
            self.title_label("First-time setup",
                             "No device profile on this pendrive yet. Scan the device you want to protect.")
            self.buttons(("Scan device", self.first_scan))
            return
        head = self.st["log"][-1]
        self.title_label("HWGuard", f"Profile v{head['seq']}  |  head hash {head['hash'][:18]}...")
        ttk.Label(self.body, text=f"{len(head['components'])} components tracked").pack(anchor="w")
        self.buttons(("Verify device", self.verify), ("Update device configuration", self.update_cfg))

    # first run
    def first_scan(self):
        self.busy("Scanning device", hs.collect, self.first_scan_done)

    def first_scan_done(self, res):
        if isinstance(res, BaseException):
            return self.scan_failed(res)
        raw, cycles, skipped = res
        self.clear()
        self.title_label("Review detected hardware",
                         "Check every line against the device. Unreadable items are NOT protected.")
        self.tree(("Type", "Slot", "Serial / ID"), raw, (120, 160, 480))
        if cycles is not None:
            ttk.Label(self.body, text=f"Battery cycle count: {cycles}").pack(anchor="w")
        if skipped:
            ttk.Label(self.body, text="Could not read: " + ", ".join(skipped),
                      foreground="#c62828", wraplength=760).pack(anchor="w")
        f = ttk.Frame(self.body)
        f.pack(anchor="w", pady=8)
        p1, p2 = tk.StringVar(), tk.StringVar()
        ttk.Label(f, text="Set password (needed to update config):").grid(row=0, column=0, sticky="w")
        ttk.Entry(f, textvariable=p1, show="*", width=28).grid(row=0, column=1, padx=6)
        ttk.Label(f, text="Confirm password:").grid(row=1, column=0, sticky="w")
        ttk.Entry(f, textvariable=p2, show="*", width=28).grid(row=1, column=1, padx=6, pady=3)

        def confirm():
            if len(p1.get()) < 8:
                return messagebox.showwarning("Weak password", "Use at least 8 characters.")
            if p1.get() != p2.get():
                return messagebox.showwarning("Mismatch", "Passwords do not match.")
            pw_salt, salt = secrets.token_hex(16), secrets.token_hex(16)
            key = derive_key(p1.get(), pw_salt)
            entry = make_entry(0, salt, raw, cycles, "0x" + "00" * 32, key, "initial scan")
            self.st = {"version": 1, "salt": salt, "pw_salt": pw_salt, "pw_tag": pw_tag(key), "log": [entry]}
            save_state(self.st)
            messagebox.showinfo("Saved", f"Profile saved.\nHead hash (anchor on-chain):\n{entry['hash']}")
            self.show_home()

        self.buttons(("Details are correct, save", confirm), ("Cancel", self.show_home))

    # verify
    def verify(self):
        self.busy("Verifying device", hs.collect, self.verify_done)

    def verify_done(self, res):
        if isinstance(res, BaseException):
            return self.scan_failed(res)
        raw, cycles, _ = res
        head = self.st["log"][-1]
        rows, notes = compare(head, raw, cycles, self.st["salt"])
        intact = chain_ok(self.st)
        bad = any(r[2] != "OK" for r in rows) or notes or not intact
        self.clear()
        if bad:
            self.title_label("TAMPER / CHANGE DETECTED")
        else:
            self.title_label("Device verified", "Every tracked component matches the stored profile.")
        self.tree(("Type", "Slot", "Status", "Current serial / ID"), rows, (110, 150, 110, 400))
        for n in notes:
            ttk.Label(self.body, text=n, foreground="#c62828").pack(anchor="w")
        if not intact:
            ttk.Label(self.body, text="State file hash-chain is BROKEN: the profile was edited.",
                      foreground="#c62828").pack(anchor="w")
        ttk.Label(self.body, text=f"Profile head: {head['hash']}").pack(anchor="w", pady=4)
        self.buttons(("Back", self.show_home))

    # update
    def update_cfg(self):
        win = tk.Toplevel(self)
        win.title("Password")
        win.grab_set()
        pw = tk.StringVar()
        ttk.Label(win, text="Enter configuration password:").pack(padx=14, pady=(14, 4))
        e = ttk.Entry(win, textvariable=pw, show="*", width=30)
        e.pack(padx=14)
        e.focus()

        def ok():
            key = derive_key(pw.get(), self.st["pw_salt"])
            if not hmac.compare_digest(pw_tag(key), self.st["pw_tag"]):
                messagebox.showerror("Denied", "Wrong password.", parent=win)
                return
            win.destroy()
            self.busy("Scanning device", hs.collect, lambda r: self.update_done(r, key))

        ttk.Button(win, text="Unlock", command=ok).pack(pady=12)
        win.bind("<Return>", lambda _e: ok())

    def update_done(self, res, key):
        if isinstance(res, BaseException):
            return self.scan_failed(res)
        raw, cycles, skipped = res
        head = self.st["log"][-1]
        rows, notes = compare(head, raw, cycles, self.st["salt"])
        self.clear()
        self.title_label("Review changes since last profile",
                         "Approving makes the current hardware the new trusted baseline (logged, not overwritten).")
        self.tree(("Type", "Slot", "Status", "Current serial / ID"), rows, (110, 150, 110, 400))
        for n in notes:
            ttk.Label(self.body, text=n, foreground="#b26a00").pack(anchor="w")
        if skipped:
            ttk.Label(self.body, text="Could not read: " + ", ".join(skipped),
                      foreground="#c62828", wraplength=760).pack(anchor="w")
        note = tk.StringVar()
        f = ttk.Frame(self.body)
        f.pack(anchor="w", pady=8)
        ttk.Label(f, text="What changed / why:").pack(side="left")
        ttk.Entry(f, textvariable=note, width=50).pack(side="left", padx=6)

        def approve():
            entry = make_entry(head["seq"] + 1, self.st["salt"], raw, cycles, head["hash"], key,
                               note.get().strip() or "config update")
            self.st["log"].append(entry)
            save_state(self.st)
            messagebox.showinfo("Updated", f"New head hash (anchor on-chain):\n{entry['hash']}")
            self.show_home()

        self.buttons(("Approve & save new configuration", approve), ("Cancel", self.show_home))


if __name__ == "__main__":
    App().mainloop()