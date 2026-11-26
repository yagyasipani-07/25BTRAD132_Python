# 25BTRAD132_Python

Comprehensive collection of Python programming coursework, lab exercises, problem-solving assignments, and experiential learning projects for **25BTRAD132**.

---

## 👨‍💻 Student Profile

- **Name:** Yagya Sipani
- **USN:** 25BTRAD132
- **Department:** Computer Science & Engineering (Artificial Intelligence and Data Engineering)
- **Institution:** Jain (Deemed-to-be University)

---

## 📁 Repository Structure

```text
25BTRAD132_Python/
│
├── 25BTRAD132_Experiential_Learning/
│   └── FINALPROJECT/                     # Capstone Experiential Project: HWGuard
│       ├── FINALPROJECT.py               # Main application engine (GUI & verification)
│       ├── HWGuard.html                  # Web/mobile inspection dashboard
│       ├── HWGuard.bat                   # Windows launcher
│       ├── HWGuard.sh                    # Linux launcher
│       ├── HWGuard.command               # macOS launcher
│       └── README.txt                    # Project documentation & usage instructions
│
├── 25BTRAD132_LAB_Exercises/
│   ├── Lab_Exercise_1.py                 # Lab 1: Python environment setup & fundamentals (.py script)
│   ├── Lab_excercise_1.ipynb             # Lab 1: Jupyter Notebook version
│   ├── Lab_Exercise_2.py                 # Lab 2: Control flow, number guessing, prime & factorials (.py script)
│   ├── Lab_Excercise_2.ipynb             # Lab 2: Jupyter Notebook version
│   ├── Lab_exercise_3.py                 # Lab 3: Data structures & Interactive Contact Book
│   ├── Lab_Exercise_4.py                 # Lab 4: File I/O, log analyzer & student database
│   └── Lab_Exercise_5.py                 # Lab 5: OOP principles (Encapsulation, Inheritance)
│
├── 25BTRAD132_Problem_Solving/
│   ├── Task1.py                          # Problem Solving Tasks 1-18 (.py script)
│   ├── Task1.ipynb                       # Problem Solving Tasks 1-18 (Jupyter Notebook)
│   ├── Bill Genrator.py                  # Retail billing generator with itemized receipts
│   ├── Sales Data Analyzer.py            # Sales records analyzer and inventory manager
│   └── OTP Generator.py                  # Cryptographic / pseudorandom OTP generator
│
├── .gitignore                            # Git ignore rules for Python & macOS
└── README.md                             # Repository documentation
```

---

## 🚀 Projects & Modules Overview

### 1. 🛡️ Experiential Learning — HWGuard Universal Hardware Vault
> **Directory:** `25BTRAD132_Experiential_Learning/FINALPROJECT/`

**HWGuard** is a portable hardware integrity and anti-tampering utility engineered to detect component swapping, RAM theft, and motherboard/disk alterations.

- **Key Highlights:**
  - **Zero Raw Data Storage:** Hashes component serials using salted Keccak-256 / SHA-256 algorithms.
  - **Tamper-Evident State Log:** Maintains an append-only, hash-chained configuration log (`state.json`).
  - **Cross-Platform Support:** Ready-to-run automation scripts for macOS (`.command`), Windows (`.bat`), Linux (`.sh`), and mobile devices (`.html`).
  - **Cryptographic Security:** Passwords derived using `scrypt` key derivation with HMAC verification.

---

### 2. 🧪 Lab Exercises
> **Directory:** `25BTRAD132_LAB_Exercises/`

A structured progression through core Python concepts and applied programming:

| File | Topics Covered | Key Concepts |
| :--- | :--- | :--- |
| **`Lab_excercise_1.ipynb`** | Environment Setup & Basics | IDE configuration (VS Code, PyCharm, Jupyter), basic I/O, syntax |
| **`Lab_Excercise_2.ipynb`** | Control Flow & Algorithms | Number guessing game, prime testing, factorial computation |
| **`Lab_exercise_3.py`** | Data Structures & Collections | Lists, tuples, sets, dictionaries, interactive CRUD **Contact Book** |
| **`Lab_Exercise_4.py`** | File Handling & Parsing | Log file analyzer (counts `ERROR`, `WARNING`, `INFO`), student record storage |
| **`Lab_Exercise_5.py`** | Object-Oriented Programming | Encapsulation (`Bank` account management), inheritance (`Library` & `Book` issue system) |

---

### 3. 💡 Problem Solving Tasks
> **Directory:** `25BTRAD132_Problem_Solving/`

Practical applications and algorithmic solutions:

- **`Bill Genrator.py`**: Interactive console-based retail checkout system calculating subtotal, 5% sales tax, and formatted billing receipts.
- **`Sales Data Analyzer.py`**: Business inventory tracker providing input validation, inventory updates, and analytical metrics (total revenue, top-selling product).
- **`OTP Generator.py`**: Configurable, randomized numerical One-Time Password generator.
- **`Task1.ipynb`**: Fundamental introductory programming tasks and formatted string printing.

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.8 or higher installed on your machine.
- Jupyter Notebook or JupyterLab (for `.ipynb` files):
  ```bash
  pip install notebook
  ```

### Running Scripts
- **Execute any Python script:**
  ```bash
  python3 "25BTRAD132_Problem_Solving/Bill Genrator.py"
  ```
- **Open Jupyter Notebooks:**
  ```bash
  jupyter notebook "25BTRAD132_Problem_Solving/Task1.ipynb"
  ```
- **Launch HWGuard (macOS / Linux / Windows):**
  - macOS: `./25BTRAD132_Experiential_Learning/FINALPROJECT/HWGuard.command`
  - Linux: `bash ./25BTRAD132_Experiential_Learning/FINALPROJECT/HWGuard.sh`
  - Windows: `.\25BTRAD132_Experiential_Learning\FINALPROJECT\HWGuard.bat`
