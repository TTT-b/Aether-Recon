#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import json
import shutil
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
         V4.3 | Hardened Recon Edition
""" + "═"*65 + f"{RESET}")

def get_next_scan_dir():
    counter = 1
    while os.path.exists(f"Aether_scan_{counter}"):
        counter += 1
    return f"Aether_scan_{counter}"

def run_step(step_num, title, command):
    """Executes a command and forces stop on interrupt"""
    print(f"{PRIMARY}{BOLD}┌──[Step {step_num}/3] {title}{RESET}")
    print(f"{ACCENT}│ Running... (Ctrl+C to Abort Full Scan){RESET}")
    start = time.time()
    try:
        # Use subprocess.run for better signal handling
        subprocess.run(command, shell=True, check=True)
        duration = round(time.time() - start, 2)
        print(f"{SUCCESS}└─╼ Completed in {duration}s.{RESET}\n")
        return True
    except subprocess.CalledProcessError:
        print(f"{ERROR}└─╼ Task failed.{RESET}\n")
        return False
    except KeyboardInterrupt:
        # This will be caught in main
        raise KeyboardInterrupt

def main():
    show_banner()
    
    # Dependencies check
    tools = {'nmap': 'nmap --version', 'ffuf': 'ffuf -V', 'whatweb': 'whatweb --version'}
    for t, cmd in tools.items():
        if subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
            print(f"{ERROR}[!] Missing {t}. Please run V4.2 repair logic.{RESET}")
            return

    target = input(f"{SECONDARY}{BOLD}» Target Host: {RESET}").strip()
    if not target: return

    base_dir = get_next_scan_dir()
    raw_dir = f"{base_dir}/raw_logs"
    os.makedirs(raw_dir, exist_ok=True)
    
    print(f"{SECONDARY}[ℹ] Session: {base_dir}{RESET}\n")
    host_clean = target.replace("http://", "").replace("https://", "").split('/')[0]
    full_url = target if target.startswith("http") else f"http://{target}"

    try:
        # Execution steps with flow control
        if not run_step(1, "Technology Fingerprinting", f"whatweb -a 3 {full_url} --color=never > {raw_dir}/tech_stack.txt"):
            pass # Keep going if one step fails, but stop on Ctrl+C
            
        run_step(2, "Service Discovery", f"nmap -sV -F {host_clean} -oN {raw_dir}/nmap_scan.txt")
        
        wordlist = "/usr/share/wordlists/dirb/common.txt"
        if os.path.exists(wordlist):
            run_step(3, "Path Discovery", f"ffuf -u {full_url}/FUZZ -w {wordlist} -mc 200,301,302 -t 40 -o {raw_dir}/ffuf_results.json")

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
