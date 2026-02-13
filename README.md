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
- **Automated Reporting**: Generates a clean Markdown summary for every scan.
- **Modern UI**: High-contrast, color-coded CLI interface for better readability.

---

## 🛠 Prerequisites

Before running Aether, ensure you have the following tools installed (Kali Linux recommended):

- **Nmap**: `sudo apt install nmap`
- **WhatWeb**: `sudo apt install whatweb`
- **FFUF**: `sudo apt install ffuf`
- **Python 3**: `sudo apt install python3`

---

## 📥 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Aether-Recon.git](https://github.com/YOUR_USERNAME/Aether-Recon.git)
   cd Aether-Recon
