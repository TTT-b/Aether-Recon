🌌 Aether Recon Suite V4.1
Aether is a modular, automated reconnaissance framework designed for fast and effective passive fingerprinting, service discovery, and path enumeration.

Built for Security Researchers, Pentesters, and Bug Bounty Hunters who need a streamlined, automated workflow to kickstart their recon phase.

🚀 Key Features
Technology Fingerprinting: Leverages WhatWeb to identify CMS, frameworks, and web server details.

Service Discovery: Uses Nmap for rapid port scanning and service version detection.

Path Fuzzing: Integrated FFUF engine with Live Output for directory and file brute-forcing.

Smart Dependency Check: Automatically detects missing/broken tools and offers to repair or install them.

Executive Reporting: Generates a smart Markdown summary that extracts the most important findings (Open ports, Tech stack, etc.) for quick review.

Recon Blue UI: Professional, high-contrast CLI interface.

🛠 Dependencies
Good News: Aether automatically checks for these tools and will offer to install them for you!

Nmap: Port scanning

WhatWeb: Technology fingerprinting

FFUF: Directory fuzzing

Python 3: Runtime environment

📥 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/TTT-b/Aether-Recon.git
cd Aether-Recon
Grant execution permissions:

Bash
chmod +x aether.py
Run the suite:

Bash
python3 aether.py
💻 Usage
Once launched, simply follow the on-screen prompts:

Enter your Target Host (e.g., example.com).

Watch the automated engines (WhatWeb, Nmap, FFUF) run in sequence.

Access your results in the newly created session folder:

Executive_Summary.md: Your "Smart" summary.

raw_logs/: Full output files from all tools.

⚠️ Disclaimer
This tool is for educational purposes and authorized testing only.
Do not use this tool on any system or network without explicit permission. The author is not responsible for any illegal use or damage caused by this tool.

Happy Hacking! 🕵️‍♂️
