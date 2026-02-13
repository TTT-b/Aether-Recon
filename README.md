# 🌌 Aether Recon Suite V3.5

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

**Aether** is a modular, automated reconnaissance framework designed for fast and effective passive fingerprinting, service discovery, and path enumeration.

Built for **Security Researchers**, **Pentesters**, and **Bug Bounty Hunters** who need a streamlined workflow to kickstart their recon phase.

---

## 🚀 Features

- **Technology Fingerprinting**: Leverages `WhatWeb` to identify CMS, frameworks, and web server details.
- **Service Discovery**: Uses `Nmap` for rapid port scanning and service version detection.
- **Path Fuzzing**: Integrated `FFUF` engine for lightning-fast directory and file brute-forcing.
- **Smart Dependency Check**: Automatically detects missing tools and offers to install them for you.
- **Automated Reporting**: Generates a clean Markdown summary for every scan.
- **Modern UI**: High-contrast, color-coded CLI interface for better readability.

---

## 🛠 Dependencies

**Good News:** Aether automatically checks for these tools and will ask to install them if they are missing! 

For transparency, here is the list of tools Aether utilizes:
- **Nmap**: Port scanning
- **WhatWeb**: Technology fingerprinting
- **FFUF**: Directory fuzzing
- **Python 3**: Runtime environment

*Note: This tool is optimized for Kali Linux but works on any Debian-based system.*

---

## 📥 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/TTT-b/Aether-Recon.git](https://github.com/TTT-b/Aether-Recon.git)
   cd Aether-Recon
Make the script executable (Optional):

Bash
chmod +x aether.py
💻 Usage
Run the tool using Python 3:

Bash
python3 aether.py
Follow the on-screen prompt to enter your target domain (e.g., example.com).
Results will be saved in a timestamped folder named Aether_TARGET_TIME.

⚠️ Disclaimer
This tool is for educational purposes and authorized testing only.
Do not use this tool on any system or network without explicit permission from the owner. The author is not responsible for any illegal use or damage caused by this tool.

Happy Hacking! 🕵️‍♂️
