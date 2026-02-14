# Aether: SOC Analyst Edition

![Version](https://img.shields.io/badge/Version-7.1-blueviolet)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**Aether** is an automated investigation framework designed for SOC Analysts and Blue Teams. It integrates network reconnaissance, web enumeration, and threat intelligence into a unified CLI tool.

## Overview

Unlike standard scanners, Aether focuses on the analyst's workflow. It offers adaptive scanning modes (Stealth vs. Aggressive) and integrates API-based threat intelligence to reduce triage time.

## Key Features

### 1. Adaptive Scanning Modes
- **Stealth Recon (Mode 1):** Uses minimal threads and timing templates (`-T2`) to evade IDS/IPS detection.
- **Standard Recon (Mode 2):** Balanced speed for routine checks.
- **Aggressive Recon (Mode 3):** Full-throttle enumeration (`-A`, `-T4`) for comprehensive data collection.

### 2. Integrated Threat Intelligence
- **AbuseIPDB Integration:** Automatically queries target reputation via API.
- **Confidence Scoring:** Returns a color-coded abuse confidence score directly to the terminal.

### 3. Resilience & Automation
- **Self-Healing Dependencies:** Automatically detects missing tools (`nmap`, `ffuf`, `whatweb`) and handles installation via `apt`.
- **Fail-Safe Interrupts:** Smart handling of `Ctrl+C` events, allowing the user to skip specific steps or abort cleanly without leaving residual files.

## Technical Stack

The tool orchestrates the following engines:
- **Network:** Nmap (Service discovery & versioning)
- **Web:** WhatWeb (Technology fingerprinting)
- **Fuzzing:** FFUF (Directory & file enumeration)
- **Intel:** cURL + AbuseIPDB API

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TTT-b/Aether-Recon.git
   cd Aether-Recon
2. Grant execution permissions:
    ```bash
    chmod +x aether.py
    ```
3. Run the tool:
    ```bash
    python3 aether.py
    ```
Note: For Threat Intelligence features, ensure you update the ```ABUSEIPDB_KEY``` variable in ```aether.py``` with your own API key.
