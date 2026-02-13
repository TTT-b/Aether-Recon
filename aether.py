#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import json
import shutil
import re
import socket  # For host validation
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
         V5.1 | The Bulletproof Edition
""" + "═"*65 + f"{RESET}")

def is_resolvable(host):
    """Checks if the host actually exists (Addressing the 'd' bug)"""
    try:
        socket.gethostbyname(host)
        return True
    except socket.gaierror:
        return False

def check_dependencies():
    tools = {'nmap': 'nmap --version', 'ffuf': 'ffuf -V', 'whatweb': 'whatweb --version'}
    missing = [t for t, cmd in tools.items() if subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0]
    if not missing: return True
    print(f"{ERROR}[!] Missing tools: {', '.join(missing)}{RESET}")
    if input(f"{ACCENT}[?] Auto-install? (Y/n): {RESET}").lower() in ['y', '']:
        os.system("sudo apt-get update -y && sudo apt-get install -y " + " ".join(missing))
        return True
    return False

def get_next_scan_dir():
    counter = 1
    while os.path.exists(f"Aether_scan_{counter}"):
        counter += 1
    return f"Aether_scan_{counter}"

def run_step(step_num, title, command, timeout=300):
    print(f"{PRIMARY}{BOLD}┌──[Step {step_num}/3] {title}{RESET}")
    print(f"{ACCENT}│ Running...{RESET}")
    start = time.time()
    try:
        subprocess.run(command, shell=True, check=True, timeout=timeout)
        duration = round(time.time() - start, 2)
        print(f"{SUCCESS}└─╼ Completed in {duration}s.{RESET}\n")
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print(f"{ERROR}└─╼ Failed. Moving on...{RESET}\n")
        return False

def main():
    show_banner()
    if not check_dependencies(): sys.exit(1)
    
    # Early Interrupt Catching
    raw_input = input(f"{SECONDARY}{BOLD}» Target Host: {RESET}").strip()
    if not raw_input: return

    target = raw_input.split()[0].rstrip('/')
    host_only = target.replace("http://", "").replace("https://", "").split('/')[0].split(':')[0]
    
    # Validating existence before folders are even created
    if not is_resolvable(host_only):
        print(f"{ERROR}[!] Error: Could not resolve host '{host_only}'. Check your connection or URL.{RESET}")
        return

    base_dir = get_next_scan_dir()
    raw_dir = f"{base_dir}/raw_logs"
    os.makedirs(raw_dir, exist_ok=True)
    
    print(f"{SECONDARY}[ℹ] Session: {base_dir} | Target: {host_only}{RESET}\n")
    full_url = target if target.startswith("http") else f"http://{target}"

    # Step Execution
    run_step(1, "Technology Fingerprinting", f"whatweb -a 3 {full_url} --color=never > {raw_dir}/tech_stack.txt")
    run_step(2, "Service Discovery", f"nmap -sV -F {host_only} -oN {raw_dir}/nmap_scan.txt")
    
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    if os.path.exists(wordlist):
        run_step(3, "Path Discovery", f"ffuf -u {full_url}/FUZZ -w {wordlist} -mc 200,301,302 -t 40 -o {raw_dir}/ffuf_results.json")

    print(f"\n{PRIMARY}{BOLD}★ Mission Accomplished ★{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{ERROR}[!] Interrupted. Exiting gracefully.{RESET}")
        # Option to cleanup if folders were created
        sys.exit(0)
