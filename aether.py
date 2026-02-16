#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import json
import shutil
import socket

# --- CONFIGURATION ---
# API Key for AbuseIPDB (Used for reputation checks)
ABUSEIPDB_KEY = "40e57a16c83beecad28a63eed160a380d227bb5e047d1e87824513686368b1ae30eb958516064458"

# --- VISUAL PALETTE (ANSI Colors) ---
PRIMARY = '\033[38;5;33m'   # Blue (Titles)
SECONDARY = '\033[38;5;45m' # Light Blue (Info)
SUCCESS = '\033[38;5;82m'   # Green (Success)
ACCENT = '\033[38;5;202m'   # Orange (Process/Warning)
ERROR = '\033[38;5;196m'    # Red (Critical Errors)
BOLD = '\033[1m'
RESET = '\033[0m'

def show_banner():
    """Clears the screen and displays the tool's banner."""
    os.system('clear' if os.name == 'posix' else 'cls')
    banner = f"{PRIMARY}{BOLD}" + "═"*65 + f"\n" + r"""
    ___      ______ ______  __  __ ______ ____  
   /   |    / ____//_   __/ / / / // ____// __ \ 
  / /| |   / __/    / /    / /_/ // __/  / /_/ / 
 / ___ |  / /___   / /    / __  // /___ / _, _/  
/_/  |_| /_____/  /_/    /_/ /_//_____//_/ |_|   
                                                 
[ Integrates: Network Recon | Web Enum | Threat Intel V7.1 ]
 ═════════════════════════════════════════════════════
    """
    print(banner)

def check_dependencies():
    """
    Verifies that all required external tools are installed.
    If a tool is missing, it prompts the user to auto-install via APT.
    """
    tools = ['nmap', 'ffuf', 'whatweb', 'curl']
    # Check if tools exist in system PATH
    missing = [t for t in tools if shutil.which(t) is None]
    
    if not missing: return True
    
    print(f"{ERROR}[!] Missing dependencies: {', '.join(missing)}{RESET}")
    try:
        # Self-Healing: Offer to fix the environment
        choice = input(f"{ACCENT}[?] Attempt auto-install via APT? (Y/n): {RESET}").lower()
        if choice in ['y', 'yes', '']:
            os.system("sudo apt-get update && sudo apt-get install -y " + " ".join(missing))
            return True
        return False
    except KeyboardInterrupt: sys.exit(0)

def get_next_scan_dir():
    """
    Manages session storage.
    Creates a new directory (Aether_scan_X) for each run to avoid overwriting data.
    """
    counter = 1
    while os.path.exists(f"Aether_scan_{counter}"):
        counter += 1
    return f"Aether_scan_{counter}"

def get_ip_reputation(target_ip):
    """
    Queries AbuseIPDB API to check if the target IP is malicious.
    Returns: JSON data containing ISP, Country, and Abuse Score.
    """
    cmd = [
        'curl', '-s', '-G', 'https://api.abuseipdb.com/api/v2/check',
        '--data-urlencode', f'ipAddress={target_ip}',
        '-d', 'maxAgeInDays=90',
        '-H', f'Key: {ABUSEIPDB_KEY}',
        '-H', 'Accept: application/json'
    ]
    try:
        # Run curl silently and capture output
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)['data']
        
        # Visual Scoring Logic
        score = data['abuseConfidenceScore']
        score_color = SUCCESS if score < 10 else (ACCENT if score < 50 else ERROR)
        
        print(f"\n{PRIMARY}{BOLD}┌──[ Threat Intel ] Reputation for {target_ip}{RESET}")
        print(f"{SECONDARY}│  ISP:{RESET} {data['isp']}")
        print(f"{SECONDARY}│  Country:{RESET} {data['countryCode']}")
        print(f"{score_color}└─╼ Abuse Score: {score}% {RESET}\n")
        return data
    except:
        print(f"{ERROR}[!] Threat Intel Failed (API Error).{RESET}")
        return None

def generate_summary(base_dir, target, intel_data):
    """
    Parses raw logs (Nmap/WhatWeb) and generates a clean 'Executive Summary'.
    This file is intended for quick triage by the analyst.
    """
    summary_path = f"{base_dir}/Scan_Summary.txt"
    with open(summary_path, "w") as f:
        f.write(f"AETHER RECON SUMMARY - {target}\n")
        f.write("="*40 + "\n\n")
        
        # Add Intel Data if available
        if intel_data:
            f.write(f"[+] Threat Intel: Score {intel_data['abuseConfidenceScore']}% ({intel_data['isp']})\n")
        
        # Parse Nmap: Extract only open ports
        nmap_path = f"{base_dir}/raw_logs/nmap.txt"
        if os.path.exists(nmap_path):
            f.write("\n[+] Open Ports & Services:\n")
            with open(nmap_path, "r") as nf:
                for line in nf:
                    if "/tcp" in line and "open" in line:
                        f.write(f"    - {line.strip()}\n")
        
        # Parse WhatWeb: Extract raw tech stack
        tech_path = f"{base_dir}/raw_logs/tech.txt"
        if os.path.exists(tech_path):
            f.write("\n[+] Technologies Detected:\n")
            with open(tech_path, "r") as tf:
                f.write(f"    {tf.read().strip()}\n")
    
    print(f"{SUCCESS}[+] Executive Summary Generated.{RESET}")

def run_step(step_num, title, command):
    """
    Generic execution engine.
    Runs shell commands with error handling and user interrupt support (Ctrl+C).
    """
    print(f"{PRIMARY}{BOLD}┌──[Step {step_num}] {title}{RESET}")
    print(f"{ACCENT}│ Running...{RESET}")
    try:
        # check=True raises an exception if the command fails
        subprocess.run(command, shell=True, check=True)
        print(f"{SUCCESS}└─╼ Completed.{RESET}\n")
        return True
    except KeyboardInterrupt:
        print(f"\n{ACCENT}[!] Step skipped by user.{RESET}")
        return False
    except:
        print(f"{ERROR}└─╼ Failed.{RESET}")
        return False

def run_whatweb_pretty(step_num, full_url, output_path):
    """
    Specialized handler for WhatWeb.
    Parses the messy raw output into a clean, readable list for the terminal,
    while saving the full raw data to a file.
    """
    print(f"{PRIMARY}{BOLD}┌──[Step {step_num}] Tech Fingerprint{RESET}")
    print(f"{ACCENT}│ Running...{RESET}")
    try:
        # Run silently (--color=never) to facilitate parsing
        cmd = f"whatweb -a 1 --color=never --no-errors {full_url}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        # Save raw output for evidence
        with open(output_path, "w") as f:
            f.write(result.stdout)
            
        # Parse output for display
        if result.stdout:
            # Clean up the output string to isolate tags
            raw_text = result.stdout.split(' [200 OK] ')[-1] if ' [200 OK] ' in result.stdout else result.stdout
            tags = raw_text.split(', ')
            
            # Print each tag nicely
            for tag in tags:
                clean_tag = tag.strip()
                if clean_tag:
                    print(f"    {SECONDARY}• {clean_tag}{RESET}")
            
        print(f"{SUCCESS}└─╼ Completed.{RESET}\n")
        return True
    except KeyboardInterrupt:
        print(f"\n{ACCENT}[!] Step skipped by user.{RESET}")
        return False
    except:
        print(f"{ERROR}└─╼ Failed.{RESET}")
        return False

def main():
    try:
        # Ensure environment is ready
        if not check_dependencies(): sys.exit(1)
        
        while True:
            show_banner()
            # --- MAIN MENU ---
            print(f"{BOLD}Select Operation Mode:{RESET}")
            print(f"  {PRIMARY}[1]{RESET} Stealth Recon    (Slow, Quiet, -T2)")
            print(f"  {PRIMARY}[2]{RESET} Standard Recon   (Default, -sV)")
            print(f"  {PRIMARY}[3]{RESET} Aggressive Recon (Full Scan, -A)")
            print(f"  {ACCENT}[4]{RESET} Threat Intel Check (API Only)")
            print(f"  {ERROR}[exit]{RESET} Quit Aether")
            
            # --- INPUT HANDLING ---
            try: mode = input(f"\n{SECONDARY}{BOLD}» Select Mode: {RESET}").strip().lower()
            except KeyboardInterrupt: break
            if mode in ['exit', 'quit']: break
            if mode not in ['1', '2', '3', '4']: continue

            target_raw = input(f"{SECONDARY}{BOLD}» Target IP/Domain: {RESET}").strip()
            if not target_raw: continue

            # --- TARGET RESOLUTION ---
            try:
                # Strip protocol to get hostname, then resolve IP
                clean_host = target_raw.replace("http://", "").replace("https://", "").split('/')[0]
                target_ip = socket.gethostbyname(clean_host)
                print(f"{SUCCESS}[+] Target Resolved: {target_ip}{RESET}")
            except:
                print(f"{ERROR}[!] Resolution failed. Check spelling.{RESET}")
                continue

            # --- THREAT INTEL CHECK ---
            # Always performed first to ensure safety/reputation
            intel_data = get_ip_reputation(target_ip)
            if mode == '4':
                input(f"{PRIMARY}Check Complete. Press Enter to return to menu...{RESET}"); continue

            # --- SETUP SESSION ---
            base_dir = get_next_scan_dir()
            raw_dir = f"{base_dir}/raw_logs"
            os.makedirs(raw_dir, exist_ok=True)

            # --- CONFIGURE ENGINES ---
            # Default: Version detection + Top 1000 ports (Standard professional check)
            nmap_args = "-sV --top-ports 1000"
            ffuf_args = "-c -mc 200,301"  # Color output, match OK/Redirect
            
            # Adjust intensity based on mode
            if mode == '1': 
                # Stealth: SYN scan, slow timing, only top 100 ports
                nmap_args = "-sS -T2 --top-ports 100" 
            elif mode == '3': 
                # Aggressive: OS detect, Scripts, Vuln scan, Fast timing
                nmap_args = "-A -T4 --script vuln" 

            full_url = target_raw if target_raw.startswith("http") else f"http://{target_raw}"
            
            # --- EXECUTION FLOW ---
            
            # Step 1: Technology Fingerprinting (WhatWeb)
            run_whatweb_pretty(1, full_url, f"{raw_dir}/tech.txt")
            
            # Step 2: Port & Service Discovery (Nmap)
            run_step(2, "Service Scan", f"nmap {nmap_args} {target_ip} -oN {raw_dir}/nmap.txt")
            
            # Step 3: Web Directory Enumeration (FFUF)
            wordlist = "/usr/share/wordlists/dirb/common.txt"
            if os.path.exists(wordlist):
                run_step(3, "Directory Enum", f"ffuf -u {full_url}/FUZZ -w {wordlist} {ffuf_args} -o {raw_dir}/ffuf.json")
            
            # Finalize: Create Report
            generate_summary(base_dir, target_raw, intel_data)
            
            input(f"\n{SUCCESS}Scan Complete. Results in {base_dir}. Press Enter to return...{RESET}")

    except KeyboardInterrupt: sys.exit(0)

if __name__ == "__main__":
    main()
