#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import re
from datetime import datetime

# --- Aether Visual Palette ---
PRIMARY, SECONDARY, SUCCESS, ACCENT, ERROR = '\033[38;5;129m', '\033[38;5;45m', '\033[38;5;82m', '\033[38;5;202m', '\033[38;5;196m'
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
         V4.0 | Professional Recon Edition
""" + "═"*65 + f"{RESET}")

def check_dependencies():
    tools = {'nmap': 'nmap --version', 'ffuf': 'ffuf -V', 'whatweb': 'whatweb --version'}
    missing = [t for t, cmd in tools.items() if subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0]
    if not missing: return True
    print(f"{ERROR}[!] Missing: {', '.join(missing)}{RESET}")
    if input(f"{ACCENT}» Install automatically? (Y/n): {RESET}").lower() in ['y', 'yes', '']:
        subprocess.run("sudo apt-get update", shell=True)
        for t in missing: os.system(f"sudo apt-get install --reinstall -y {t}")
        return True
    return False

def run_step(step_num, title, command):
    print(f"{PRIMARY}{BOLD}┌──[Step {step_num}/3] {title}{RESET}")
    start = time.time()
    exit_code = os.system(command)
    duration = round(time.time() - start, 2)
    status = f"{SUCCESS}Completed" if exit_code == 0 else f"{ERROR}Failed"
    print(f"{SUCCESS if exit_code == 0 else ERROR}└─╼ {status} in {duration}s.{RESET}\n")

def parse_nmap(file_path):
    """Extracts open ports from Nmap text file"""
    ports = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                if "/tcp" in line and "open" in line:
                    ports.append(line.strip())
    return ports

def create_smart_report(base_dir, raw_dir, target):
    """Generates a beautiful summary report by parsing raw logs"""
    report_path = f"{base_dir}/Executive_Summary.md"
    
    # Extract data from raw files
    open_ports = parse_nmap(f"{raw_dir}/nmap_scan.txt")
    
    with open(report_path, 'w') as f:
        f.write(f"# 🛡️ Recon Report: {target}\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## 🌐 Network Services (Nmap)\n")
        if open_ports:
            f.write("Found the following open ports:\n")
            for port in open_ports: f.write(f"- `{port}`\n")
        else:
            f.write("- No open ports discovered.\n")
            
        f.write("\n## 🛠️ Technology Stack (WhatWeb)\n")
        f.write(f"Detailed stack info saved in `{raw_dir}/tech_stack.txt`\n")
        
        f.write("\n## 📂 Discovered Paths (FFUF)\n")
        f.write(f"Directory fuzzing results available in `{raw_dir}/ffuf_results.json`\n")
        
    print(f"{SUCCESS}[+] Professional report generated: {report_path}{RESET}")

def main():
    show_banner()
    if not check_dependencies(): sys.exit(1)
    
    target = input(f"{SECONDARY}{BOLD}» Target Host: {RESET}").strip()
    if not target: return

    # Better Directory Logic
    host_clean = target.replace("http://", "").replace("https://", "").split('/')[0].replace(".", "_")
    base_dir = f"Aether_{host_clean}_{datetime.now().strftime('%H%M')}"
    raw_dir = f"{base_dir}/raw_logs"
    
    os.makedirs(raw_dir, exist_ok=True)
    print(f"{SECONDARY}[ℹ] Session organized in: {base_dir}{RESET}\n")

    full_url = target if target.startswith("http") else f"http://{target}"

    # Step 1: Tech
    run_step(1, "Technology Fingerprinting", f"whatweb -a 3 {full_url} --color=never > {raw_dir}/tech_stack.txt")
    
    # Step 2: Nmap
    run_step(2, "Service Discovery", f"nmap -sV -F {host_clean.replace('_', '.')} -oN {raw_dir}/nmap_scan.txt")
    
    # Step 3: FFUF
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    if os.path.exists(wordlist):
        run_step(3, "Path Discovery", f"ffuf -u {full_url}/FUZZ -w {wordlist} -mc 200,301,302 -t 40 -o {raw_dir}/ffuf_results.json -s")
    
    # Smart Reporting
    create_smart_report(base_dir, raw_dir, target)
    print(f"\n{ACCENT}{BOLD}★ Mission Accomplished ★{RESET}")

if __name__ == "__main__":
    main()
