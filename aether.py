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
         V5.0 | The Interview-Ready Edition
""" + "═"*65 + f"{RESET}")

def check_dependencies():
    """Verify required tools are installed (Addressing Claude's feedback)"""
    tools = {'nmap': 'nmap --version', 'ffuf': 'ffuf -V', 'whatweb': 'whatweb --version'}
    missing = []
    for t, cmd in tools.items():
        if subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
            missing.append(t)
    
    if not missing: return True
    
    print(f"{ERROR}[!] Missing tools: {', '.join(missing)}{RESET}")
    if input(f"{ACCENT}[?] Attempt auto-install? (Y/n): {RESET}").lower() in ['y', '']:
        os.system("sudo apt-get update -y")
        for t in missing: os.system(f"sudo apt-get install -y {t}")
        return True
    return False

def get_next_scan_dir():
    counter = 1
    while os.path.exists(f"Aether_scan_{counter}"):
        counter += 1
    return f"Aether_scan_{counter}"

def run_step(step_num, title, command, timeout=300):
    """Executes a command with timeout and signal handling"""
    print(f"{PRIMARY}{BOLD}┌──[Step {step_num}/3] {title}{RESET}")
    print(f"{ACCENT}│ Running... (Ctrl+C to Abort Full Scan){RESET}")
    start = time.time()
    try:
        # Added timeout logic to prevent hanging
        subprocess.run(command, shell=True, check=True, timeout=timeout)
        duration = round(time.time() - start, 2)
        print(f"{SUCCESS}└─╼ Completed in {duration}s.{RESET}\n")
        return True
    except subprocess.TimeoutExpired:
        print(f"{ERROR}└─╼ Task timed out after {timeout}s.{RESET}\n")
    except (subprocess.CalledProcessError, KeyboardInterrupt):
        raise KeyboardInterrupt
    return False

def create_final_report(base_dir, raw_dir, target):
    """Generates a structured report (The 'Brain' of the tool)"""
    report_path = f"{base_dir}/Executive_Summary.md"
    try:
        with open(report_path, 'w') as f:
            f.write(f"# 🛡️ Aether Recon Report: {target}\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## 🛠️ Summary of Findings\n")
            f.write(f"Detailed logs are available in the `{raw_dir}` directory.\n")
        print(f"{SUCCESS}[+] Professional report generated: {report_path}{RESET}")
    except Exception as e:
        print(f"{ERROR}[!] Could not generate report: {e}{RESET}")

def main():
    show_banner()
    if not check_dependencies(): sys.exit(1)
    
    raw_input = input(f"{SECONDARY}{BOLD}» Target Host: {RESET}").strip()
    if not raw_input: return

    # Improved Validation (Ports included)
    target = raw_input.split()[0].rstrip('/')
    host_only = target.replace("http://", "").replace("https://", "").split('/')[0]
    
    if not re.match(r"^[a-zA-Z0-9.-]+(:[0-9]+)?$", host_only):
        print(f"{ERROR}[!] Invalid target format.{RESET}")
        return

    base_dir = get_next_scan_dir()
    raw_dir = f"{base_dir}/raw_logs"
    os.makedirs(raw_dir, exist_ok=True)
    
    print(f"{SECONDARY}[ℹ] Target: {target} | Session: {base_dir}{RESET}\n")
    full_url = target if target.startswith("http") else f"http://{target}"

    try:
        run_step(1, "Technology Fingerprinting", f"whatweb -a 3 {full_url} --color=never > {raw_dir}/tech_stack.txt")
        run_step(2, "Service Discovery", f"nmap -sV -F {host_only.split(':')[0]} -oN {raw_dir}/nmap_scan.txt")
        
        # Wordlist Path Logic (Claude's feedback)
        wordlists = ["/usr/share/wordlists/dirb/common.txt", "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"]
        active_wl = next((w for w in wordlists if os.path.exists(w)), None)
        
        if active_wl:
            run_step(3, "Path Discovery", f"ffuf -u {full_url}/FUZZ -w {active_wl} -mc 200,301,302 -t 40 -o {raw_dir}/ffuf_results.json")
        else:
            print(f"{ACCENT}[!] No common wordlists found. Skipping Step 3.{RESET}")

        create_final_report(base_dir, raw_dir, target)
        print(f"\n{PRIMARY}{BOLD}★ Mission Accomplished ★{RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{ERROR}[!] Scan Aborted.{RESET}")
        if input(f"{ACCENT}[?] Delete folder '{base_dir}'? (y/N): {RESET}").lower() == 'y':
            shutil.rmtree(base_dir)
        sys.exit(0)

if __name__ == "__main__":
    main()
