#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import json
import shutil
import re
import socket
from datetime import datetime

# --- Aether Visual Palette ---
PRIMARY, SECONDARY, SUCCESS, ACCENT, ERROR = '\033[38;5;33m', '\033[38;5;45m', '\033[38;5;82m', '\033[38;5;202m', '\033[38;5;196m'
BOLD, RESET = '\033[1m', '\033[0m'

def show_banner():
    """Display the professional ASCII banner"""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{PRIMARY}{BOLD}" + "═"*65 + f"\n" + """
█████╗ ███████╗████████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗
███████║█████╗     ██║   ███████║█████╗  ██████╔╝
██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗
██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
         V5.0 | Gold Standard Edition
""" + "═"*65 + f"{RESET}")

def check_dependencies():
    """Smart check with Force-Run capability"""
    tools = ['nmap', 'ffuf', 'whatweb']
    missing = [t for t in tools if shutil.which(t) is None]
            
    if not missing:
        return True
        
    print(f"{ERROR}[!] Missing or undetected dependencies: {', '.join(missing)}{RESET}")
    
    choice = input(f"{ACCENT}[?] Attempt auto-install via APT? (Y/n): {RESET}").lower()
    if choice in ['y', '']:
        print(f"{ACCENT}[*] Fixing/Installing components...{RESET}")
        os.system("sudo apt-get update -y && sudo apt-get install --reinstall -y " + " ".join(missing))
    
    still_missing = [t for t in tools if shutil.which(t) is None]
    if still_missing:
        print(f"\n{ERROR}[!] Warning: Tools still checking as missing: {', '.join(still_missing)}{RESET}")
        force = input(f"{ACCENT}[?] Proceed anyway (Force Run)? (Y/n): {RESET}").lower()
        if force in ['y', '']: return True
        return False
    return True

def is_resolvable(host):
    """Verify DNS resolution"""
    try:
        socket.gethostbyname(host)
        return True
    except socket.gaierror:
        return False

def get_next_scan_dir():
    """Sequential directory naming"""
    counter = 1
    while os.path.exists(f"Aether_scan_{counter}"):
        counter += 1
    return f"Aether_scan_{counter}"

def run_step(step_num, title, command, timeout=300):
    """Run a command with visual feedback"""
    print(f"{PRIMARY}{BOLD}┌──[Step {step_num}/3] {title}{RESET}")
    print(f"{ACCENT}│ Running...{RESET}")
    start = time.time()
    try:
        subprocess.run(command, shell=True, check=True, timeout=timeout)
        duration = round(time.time() - start, 2)
        print(f"{SUCCESS}└─╼ Completed in {duration}s.{RESET}\n")
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        print(f"{ERROR}└─╼ Step failed or interrupted. Proceeding...{RESET}\n")
        return False

def generate_report(base_dir, target):
    """Generates the Executive Summary Markdown file"""
    report_path = f"{base_dir}/Summary_Report.md"
    raw_dir = f"{base_dir}/raw_logs"
    
    try:
        with open(report_path, 'w') as f:
            f.write(f"# 🛡️ Aether Recon Report: {target}\n")
            f.write(f"**Scan Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("---\n\n")
            
            # 1. Tech Stack
            f.write("## 🏗️ Technology Stack\n")
            if os.path.exists(f"{raw_dir}/tech_stack.txt"):
                with open(f"{raw_dir}/tech_stack.txt", 'r') as tech:
                    f.write(f"```\n{tech.read().strip()[:500]}\n```\n") # Limit size
            else:
                f.write("_No data collected._\n")

            # 2. Open Ports
            f.write("\n## 🌐 Open Ports & Services\n")
            if os.path.exists(f"{raw_dir}/nmap_scan.txt"):
                with open(f"{raw_dir}/nmap_scan.txt", 'r') as nmap:
                    content = nmap.read()
                    # Simple grep for open ports
                    ports = [line for line in content.splitlines() if "/tcp" in line and "open" in line]
                    if ports:
                        for p in ports: f.write(f"- `{p}`\n")
                    else:
                        f.write("_No open ports found or scan failed._\n")
            
            # 3. Directories
            f.write("\n## 📂 Discovered Paths (Top 5)\n")
            if os.path.exists(f"{raw_dir}/ffuf_results.json"):
                try:
                    with open(f"{raw_dir}/ffuf_results.json", 'r') as ffuf:
                        data = json.load(ffuf)
                        count = 0
                        for res in data.get('results', []):
                            if count < 5:
                                f.write(f"- `/{res['input']['FUZZ']}` (Status: {res['status']})\n")
                                count += 1
                except: f.write("_Error parsing JSON._\n")
            else:
                f.write("_No paths found._\n")
                
        print(f"{SUCCESS}[+] Executive Summary generated: {report_path}{RESET}")
        
    except Exception as e:
        print(f"{ERROR}[!] Failed to generate report: {e}{RESET}")

def main():
    show_banner()
    
    # Initialize base_dir for cleanup logic
    base_dir = None

    try:
        # 1. Dependency Validation
        if not check_dependencies(): 
            print(f"{ERROR}[!] Aborted by user.{RESET}")
            sys.exit(1)
        
        # 2. Target Input
        raw_input = input(f"{SECONDARY}{BOLD}» Target Host: {RESET}").strip()
        if not raw_input: return

        target = raw_input.split()[0].rstrip('/')
        host_only = target.replace("http://", "").replace("https://", "").split('/')[0].split(':')[0]
        
        # 3. Connectivity Pre-check
        if not is_resolvable(host_only):
            print(f"{ERROR}[!] Resolution Error: Could not resolve '{host_only}'. Check connection.{RESET}")
            return

        # 4. Workspace Setup
        base_dir = get_next_scan_dir()
        raw_dir = f"{base_dir}/raw_logs"
        os.makedirs(raw_dir, exist_ok=True)
        
        print(f"{SECONDARY}[ℹ] Session: {base_dir} | Target: {host_only}{RESET}\n")
        full_url = target if target.startswith("http") else f"http://{target}"

        # 5. Execution Pipeline
        run_step(1, "Technology Fingerprinting", f"whatweb -a 3 {full_url} --color=never > {raw_dir}/tech_stack.txt")
        run_step(2, "Service Discovery", f"nmap -sV -F {host_only} -oN {raw_dir}/nmap_scan.txt")
        
        wordlist = "/usr/share/wordlists/dirb/common.txt"
        if os.path.exists(wordlist):
            run_step(3, "Path Discovery", f"ffuf -u {full_url}/FUZZ -w {wordlist} -mc 200,301,302 -t 40 -o {raw_dir}/ffuf_results.json")
        else:
            print(f"{ACCENT}[!] Wordlist not found. Skipping Path Discovery.{RESET}")

        # 6. Report Generation
        generate_report(base_dir, target)

        print(f"\n{PRIMARY}{BOLD}★ Mission Accomplished ★{RESET}")
        print(f"{SECONDARY}[ℹ] Results saved in: {base_dir}{RESET}")

    # --- Cleanup Logic on Interrupt ---
    except KeyboardInterrupt:
        print(f"\n\n{ERROR}[!] Interrupted by user.{RESET}")
        
        # Check if folder was created
        if base_dir and os.path.exists(base_dir):
            choice = input(f"{ACCENT}[?] Scan incomplete. Delete session folder '{base_dir}'? (Y/n): {RESET}").lower()
            if choice in ['y', '']:
                shutil.rmtree(base_dir)
                print(f"{SUCCESS}[+] Folder deleted successfully.{RESET}")
            else:
                print(f"{SECONDARY}[ℹ] Partial results kept in '{base_dir}'.{RESET}")
        
        sys.exit(0)

if __name__ == "__main__":
    main()
