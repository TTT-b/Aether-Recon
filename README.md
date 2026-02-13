# 🌌 Aether Recon Suite V5.0

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

**Aether** is a modular, automated reconnaissance framework designed for fast and effective passive fingerprinting, service discovery, and path enumeration. 

Built for **Security Researchers**, **Pentesters**, and **Bug Bounty Hunters** who need a streamlined, automated workflow to kickstart their recon phase.

## 🚀 Key Features

* **Technology Fingerprinting**: Leverages `WhatWeb` to identify CMS, frameworks, and web server details.
* **Service Discovery**: Uses `Nmap` for rapid port scanning and service version detection.
* **Path Fuzzing**: Integrated `FFUF` engine with **Live Output** for real-time directory and file brute-forcing.
* **Smart Dependency Check**: Automatically detects missing/broken tools and offers to repair or install them.
* **Executive Reporting**: Generates a smart Markdown summary that extracts the most important findings for quick review.
* **Recon Blue UI**: Professional, high-contrast CLI interface designed for terminal efficiency.


## 🛠 Dependencies

**Good News:** Aether automatically checks for these tools and will offer to install/repair them for you! 

* **Nmap**: Service and port scanning.
* **WhatWeb**: Deep technology fingerprinting.
* **FFUF**: High-speed directory fuzzing.
* **Python 3**: Core runtime environment.

> **Note:** This tool is optimized for Kali Linux but works on any Debian-based system.


## 📥 Installation

1. **Clone the repository + Grant execution permissions:**
```bash
git clone https://github.com/TTT-b/Aether-Recon.git
cd Aether-Recon
chmod +x aether.py
```
2. **Usage**
Run the suite using Python3:
```bash
python3 aether.py
```
🔍 How it Works
Target Input: Follow the on-screen prompt to enter your Target Host (e.g., example.com).

Automated Scanning: Watch the engines run in sequence with live feedback.

Smart Results: Access your organized results in the session folder:

Executive_Summary.md: Your "Smart" human-readable summary.

raw_logs/: Full, unedited output files from all tools for deep analysis.

⚠️ Disclaimer
This tool is for educational purposes and authorized testing only.
Do not use this tool on any system or network without explicit permission. The author is not responsible for any illegal use or damage caused by this tool.

Happy Hacking! 🕵️‍♂️
