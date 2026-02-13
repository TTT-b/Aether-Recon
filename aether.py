#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import json
import shutil
import re
from datetime import datetime

# --- Aether Visual Palette ---
PRIMARY, SECONDARY, SUCCESS, ACCENT, ERROR = '\033[38;5;33m', '\033[38;5;45m', '\033[38;5;82m', '\033[38;5;202m', '\033[38;5;196m'
BOLD, RESET = '\033[1m', '\033[0m'

def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{PRIMARY}{BOLD}" + "═"*65 + f"\n" + """
█████╗ ███████╗████████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗
███████║█████╗     ██║   ███████║█████╗  ██████╔╝
██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗
██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
         V4.4 | Sanitized Recon Edition
""" + "═"*65 + f"{RESET}")

def get_next_scan_dir():
    counter = 1
    while os.path.exists(f"Aether_scan_{counter}"):
        counter += 1
    return f"Aether_scan_{counter}"

def run_step(step_num, title, command):
    print(f"{PRIMARY}{BOLD}┌──[Step {step_num}/3] {title}{RESET}")
    print(f"{ACCENT}│ Running... (Ctrl+C to Abort Full Scan){RESET}")
    start = time.time()
    try:
        # We wrap the command to handle signals better
        subprocess.run(command, shell=True, check=True)
        duration = round(time.time() - start, 2)
        print(f"{SUCCESS}└─╼ Completed in {duration}s.{RESET}\n")
        return True
    except subprocess.CalledProcessError:
        print(f"{ERROR}└─╼ Task failed (Check your target URL).{RESET}\n")
        return False
    except KeyboardInterrupt:
        raise KeyboardInterrupt

def main():
    show_banner()
    
    # Target Input + Sanitization
    raw_input = input(f"{SECONDARY}{BOLD}» Target Host: {RESET}").strip()
    if not raw_input: return

    # FIX: Take only the first word (the URL) and remove any trailing noise/spaces
    target = raw_input.split()[0].rstrip('/')
    
    # Double-check it's a valid-looking host
    host_only = target.replace("http://", "").replace("https://", "").split('/')[0]
    if not re.match(r"^[a-zA-Z0-9.-]+$", host_only):
        print(f"{ERROR}[!] Error: Invalid characters in target host.{RESET}")
        return

    base_dir = get_next_scan_dir()
    raw_dir = f"{base_dir}/raw_logs"
    os.makedirs(raw_dir, exist_ok=True)
    
    print(f"{SECONDARY}[ℹ] Cleaned Target: {target}{RESET}")
    print(f"{SECONDARY}[ℹ] Session: {base_dir}{RESET}\n")
    
    full_url = target if target.startswith("http") else f"http://{target}"

    try:
        # Step 1: Tech
        run_step(1, "Technology Fingerprinting", f"whatweb -a 3 {full_url} --color=never > {raw_dir}/tech_stack.txt")
        
        # Step 2: Nmap
        run_step(2, "Service Discovery", f"nmap -sV -F {host_only} -oN {raw_dir}/nmap_scan.txt")
        
        # Step 3: FFUF
        wordlist = "/usr/share/wordlists/dirb/common.txt"
        if os.path.exists(wordlist):
            run_step(3, "Path Discovery", f"ffuf -u {full_url}/FUZZ -w {wordlist} -mc 200,301,302 -t 40 -o {raw_dir}/ffuf_results.json")

        # In a real script, we would call the report function here (omitted for brevity)
        print(f"\n{PRIMARY}{BOLD}★ Mission Accomplished. Results: {base_dir} ★{RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{ERROR}[!] Scan Aborted by User.{RESET}")
        choice = input(f"{ACCENT}[?] Delete partial session folder '{base_dir}'? (y/N): {RESET}").lower()
        if choice == 'y':
            shutil.rmtree(base_dir)
            print(f"{SUCCESS}[+] Deleted.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
    
