# 🔭 Aether: SOC Analyst Edition

![Version](https://img.shields.io/badge/Version-6.0-blueviolet)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB)
![Focus](https://img.shields.io/badge/Focus-SOC%20%26%20Intel-00C853)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**Aether** is an intelligent, automated investigation framework designed specifically for **SOC Analysts** and **Blue Teamers**. 

Unlike standard "noisy" scanners, Aether offers a **tactical menu** allowing you to choose between stealthy reconnaissance, aggressive enumeration, or pure threat intelligence gathering via API integrations.

---

## 🔮 Core Capabilities

### 🛡️ Adaptive Scanning Modes
* **Stealth Recon (Mode 1):** Low-and-slow scanning (`-T2`) to evade IDS/IPS detection. Quietly maps the perimeter.
* **Standard Recon (Mode 2):** Balanced speed and depth for routine checks.
* **Aggressive Recon (Mode 3):** Full-throttle enumeration (`-A`, `-T4`) for comprehensive data collection in permissive environments.

### 🌐 Integrated Threat Intelligence
* **AbuseIPDB Integration:** Automatically queries the reputation of your target IP.
* **Visual Scoring:** Delivers a color-coded confidence score (Green/Orange/Red) directly in the terminal to speed up triage.

### 🧩 Smart Workflow
* **Self-Healing Dependencies:** Detects missing tools (`nmap`, `ffuf`, etc.) and offers to auto-install them via `apt`.
* **Fail-Safe Interrupts:** Pressed `Ctrl+C` by mistake? Aether creates a safety checkpoint, asking if you want to **skip the current step** or **abort the entire scan** and clean up the files.

---

## 🧰 The Tech Stack

Aether acts as a smart orchestrator for industry-standard tools:

* **Network:** `Nmap` (Service discovery & versioning)
* **Web:** `WhatWeb` (Technology fingerprinting & CMS detection)
* **Fuzzing:** `FFUF` (Directory & file enumeration)
* **Intel:** `cURL` + AbuseIPDB API

---

## 📥 Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/TTT-b/Aether-Recon.git](https://github.com/TTT-b/Aether-Recon.git)
    cd Aether-Recon
    ```

2.  **Make it executable:**
    ```bash
    chmod +x aether.py
    ```

3.  **Run the tool:**
    ```bash
    python3 aether.py
    ```

> **⚡ Pro Tip:** Open `aether.py` and replace `ABUSEIPDB_KEY` with your own API key to get fresh threat data!

---

## 🕹️ Usage Guide

Once launched, Aether presents a tactical dashboard:

```text
Select Operation Mode:
  [1] Stealth Recon     (Slow, Quiet, -T2)
  [2] Standard Recon    (Default, -sV)
  [3] Aggressive Recon  (Loud, Full Scan, -A)
  [4] Threat Intel Check (API Only)
