🌌 Aether Recon Suite V4.1
Aether is a modular, automated reconnaissance framework designed for fast and effective passive fingerprinting, service discovery, and path enumeration.

Built for Security Researchers, Pentesters, and Bug Bounty Hunters who need a streamlined, automated workflow to kickstart their recon phase.

🚀 Features
Technology Fingerprinting: Leverages WhatWeb to identify CMS, frameworks, and web server details.

Service Discovery: Uses Nmap for rapid port scanning and service version detection.

Path Fuzzing: Integrated FFUF engine with Live Output for real-time directory and file brute-forcing.

Smart Dependency Check: Automatically detects missing/broken tools and offers to repair or install them.

Executive Reporting: Generates a smart Markdown summary that extracts the most important findings (Open ports, Tech stack, etc.) for quick review.

Recon Blue UI: Professional, high-contrast CLI interface designed for terminal efficiency.

🛠 Dependencies
Good News: Aether automatically checks for these tools and will offer to install/repair them for you!

For transparency, here is the list of tools Aether utilizes:

Nmap: Service and port scanning.

WhatWeb: Deep technology fingerprinting.

FFUF: High-speed directory fuzzing.

Python 3: Core runtime environment.

Note: This tool is optimized for Kali Linux but works on any Debian-based system.

📥 Installation
Clone the repository:

Bash
git clone https://github.com/TTT-b/Aether-Recon.git
cd Aether-Recon
Grant execution permissions:

Bash
chmod +x aether.py
💻 Usage
Run the suite using Python 3:

Bash
python3 aether.py
🔍 How it works:
Follow the on-screen prompt to enter your Target Host (e.g., example.com).

Watch the automated engines run in sequence with live feedback.

Access your results in the session folder:

Executive_Summary.md: Your "Smart" human-readable summary.

raw_logs/: Full, unedited output files from all tools for deep analysis.
