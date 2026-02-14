#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import json
import shutil
import socket
from datetime import datetime

# --- CONFIGURATION ---
ABUSEIPDB_KEY = "40e57a16c83beecad28a63eed160a380d227bb5e047d1e87824513686368b1ae30eb958516064458"

# --- Aether Visual Palette ---
PRIMARY = '\033[38;5;33m'   # Blue
SECONDARY = '\033[38;5;45m' # Light Blue
SUCCESS = '\033[38;5;82m'   # Green
ACCENT = '\033[38;5;202m'   # Orange
ERROR = '\033[38;5;196m'    # Red
BOLD = '\033[1m'
RESET = '\033[0m'

def show_banner():
    """Display the AETHER banner"""
    os.system('clear' if os.name == 'posix' else 'cls')
    banner = f"{PRIMARY}{BOLD}" + "═"*65 + f"\n" + r"""
    ___      ______ ______  __  __ ______ ____  
   /   |    / ____//_   __/ / / / // ____// __ \ 
  / /| |   / __/    / /    / /_/ // __/  / /_/ / 
 / ___ |  / /___   / /    / __  // /___ / _, _/  
/_/  |_| /_____/  /_/    /_/ /_//_____//_/ |_|   
                                                 
           [ SOC Analyst Edition V6.0 ]
   Integrates: Network Recon | Web Enum | Threat Intel
 ═════════════════════════════════════════════════════
    """
    print(banner)

def check_dependencies():
    """Checks for tools and prompts for auto-installation."""
    tools = ['nmap', 'ffuf', 'whatweb', 'curl']
    missing = [t for t in tools if shutil.which(t) is None]
    
    if not missing:
        return True
        
    print(f"{ERROR}[!] Missing dependencies: {', '.join(missing)}{RESET}")
    
    # Ask user for auto-install
    try:
        choice = input(f"{ACCENT}[?] Attempt auto-install via APT? (Y/n): {RESET}").lower()
        if choice in ['y', 'yes', '']:
            print(f"{SECONDARY}[*] Running installation... (Requires Sudo){RESET}")
            
            # Construct command: sudo apt-get update && sudo apt-get install -y <tools>
            cmd = "sudo apt-get update && sudo apt-get install -y " + " ".join(missing)
            os.system(cmd)
            
            # Verify installation success
            still_missing = [t for t in tools if shutil.which(t) is None]
            if not still_missing:
                print(f"{SUCCESS}[+] Installation successful. Proceeding...{RESET}\n")
                time.sleep(1)
                return True
            else:
                print(f"{ERROR}[!] Installation failed for: {', '.join(still_missing)}{RESET}")
                return False
        else:
            print(f"{SECONDARY}[ℹ] Please install manually: sudo apt install {' '.join(missing)}{RESET}")
            return False
    except KeyboardInterrupt:
        sys.exit(0)

def get_ip_reputation(target_ip):
    print(f"\n{PRIMARY}{BOLD}┌──[ Threat Intel ] Checking Reputation for {target_ip}...{RESET}")
    cmd = [
        'curl', '-s', '-G', 'https://api.abuseipdb.com/api/v2/check',
        '--data-urlencode', f'ipAddress={target_ip}',
        '-d', 'maxAgeInDays=90',
        '-H', f'Key: {ABUSEIPDB_KEY}',
        '-H', 'Accept: application/json'
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        if 'errors' in data:
            print(f"{ERROR}└─╼ API Error: {data['errors'][0]['detail']}{RESET}")
            return
        data = data['data']
        score = data['abuseConfidenceScore']
        score_color = SUCCESS if score < 10 else (ACCENT if score < 50 else ERROR)
        print(f"{SECONDARY}│  {BOLD}ISP:{RESET} {data['isp']}")
        print(f"{SECONDARY}│  {BOLD}Country:{RESET} {data['countryCode']}")
        print(f"{SECONDARY}│  {BOLD}Total Reports:{RESET} {data['totalReports']}")
        print(f"{score_color}└─╼ Abuse Score: {score}% {RESET}\n")
    except:
        print(f"{ERROR}└─╼ Failed to fetch threat intel.{RESET}\n")

def get_next_scan_dir():
    counter = 1
    while os.path.exists(f"Aether_scan_{counter}"): counter += 1
    return f"Aether_scan_{counter}"

def run_step(step_num, title, command):
    """
    Runs a command. If Ctrl+C is pressed, asks user whether to skip step or abort all.
    Returns: True if completed, False if skipped, Raises KeyboardInterrupt if abort.
    """
    print(f"{PRIMARY}{BOLD}┌──[Step {step_num}] {title}{RESET}")
    print(f"{ACCENT}│ Running...{RESET}")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"{SUCCESS}└─╼ Completed.{RESET}\n")
        return True
    except KeyboardInterrupt:
        print(f"\n{ACCENT}[!] Step interrupted.{RESET}")
        choice = input(f"{SECONDARY}   » Skip this step only? (y/N - Abort Scan): {RESET}").lower()
        if choice == 'y':
            print(f"{ACCENT}   » Skipping to next step...{RESET}\n")
            return False # Continue to next step
        else:
            raise KeyboardInterrupt # Propagate 'Abort' to main
    except subprocess.CalledProcessError:
        print(f"{ERROR}└─╼ Step failed (Tool Error).{RESET}\n")
        return False

def main():
    try:
        # Check dependencies first. If failed or denied, exit.
        if not check_dependencies(): sys.exit(1)

        while True:
            show_banner()
            print(f"{BOLD}Select Operation Mode:{RESET}")
            print(f"  {PRIMARY}[1]{RESET} Stealth Recon    (Slow, Quiet, -T2)")
            print(f"  {PRIMARY}[2]{RESET} Standard Recon   (Default, -sV)")
            print(f"  {PRIMARY}[3]{RESET} Aggressive Recon (Loud, Full Scan, -A)")
            print(f"  {ACCENT}[4]{RESET} Threat Intel Check (API Only)")
            print(f"  {ERROR}[exit]{RESET} Quit Aether")
            
            # --- SAFE INPUT HANDLING ---
            try:
                mode = input(f"\n{SECONDARY}{BOLD}» Select Mode: {RESET}").strip().lower()
            except KeyboardInterrupt:
                sys.exit(0)

            if mode in ['exit', 'quit']:
                print(f"{ACCENT}[*] Exiting Aether.{RESET}")
                break

            if mode not in ['1', '2', '3', '4']:
                print(f"{ERROR}[!] Invalid selection. Try again.{RESET}")
                time.sleep(0.5)
                continue

            # --- TARGET INPUT HANDLING ---
            try:
                target_raw = input(f"{SECONDARY}{BOLD}» Target IP/Domain (or 'exit'): {RESET}").strip()
            except KeyboardInterrupt:
                sys.exit(0)

            if target_raw.lower() in ['exit', 'quit']:
                print(f"{ACCENT}[*] Exiting Aether...{RESET}")
                break
            if not target_raw: continue

            # Resolve Target
            try:
                clean_host = target_raw.replace("http://", "").replace("https://", "").split('/')[0]
                target_ip = socket.gethostbyname(clean_host)
                print(f"{SUCCESS}[+] Resolved {clean_host} -> {target_ip}{RESET}")
            except:
                print(f"{ERROR}[!] Could not resolve host.{RESET}")
                input(f"\nPress Enter to try again...")
                continue

            # --- EXECUTION ---
            if mode == '4':
                get_ip_reputation(target_ip)
                input(f"{PRIMARY}Check Complete. Press Enter to return to menu...{RESET}")
                continue

            # Create Directory
            base_dir = get_next_scan_dir()
            raw_dir = f"{base_dir}/raw_logs"
            os.makedirs(raw_dir, exist_ok=True)

            nmap_args = "-sV -F"
            ffuf_args = "-t 40"
            
            if mode == '1': nmap_args = "-sS -T2 --top-ports 100"; ffuf_args = "-t 10 -p 0.1"
            elif mode == '3': nmap_args = "-A -T4"; ffuf_args = "-t 80"

            # SCAN FLOW WITH ABORT HANDLING
            try:
                get_ip_reputation(target_ip)
                
                full_url = target_raw if target_raw.startswith("http") else f"http://{target_raw}"
                
                # Step 1
                run_step(1, "Tech Fingerprint", f"whatweb -a 1 {full_url} > {raw_dir}/tech.txt")
                
                # Step 2
                run_step(2, "Service Scan", f"nmap {nmap_args} {target_ip} -oN {raw_dir}/nmap.txt")
                
                # Step 3
                wordlist = "/usr/share/wordlists/dirb/common.txt"
                if os.path.exists(wordlist):
                    run_step(3, "Directory Enum", f"ffuf -u {full_url}/FUZZ -w {wordlist} {ffuf_args} -mc 200,301 -o {raw_dir}/ffuf.json")
                
                print(f"{SUCCESS}[+] Scan Complete. Results in: {base_dir}{RESET}")
                input(f"\nPress Enter to return to menu...")

            except KeyboardInterrupt:
                # If user chose to Abort All inside run_step
                print(f"\n\n{ERROR}[!] Full Scan Aborted by user.{RESET}")
                
                # Cleanup option
                confirm = input(f"{ACCENT}[?] Delete incomplete folder '{base_dir}'? (Y/n): {RESET}").lower()
                if confirm in ['y', 'yes', '']:
                    shutil.rmtree(base_dir)
                    print(f"{SUCCESS}[+] Cleanup done.{RESET}")
                else:
                    print(f"{SECONDARY}[ℹ] Partial data kept in {base_dir}{RESET}")
                
                time.sleep(1)
                # Loop will restart naturally
            
    except KeyboardInterrupt:
        print(f"\n\n{ACCENT}[!] User Interrupted. Exiting safely.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
