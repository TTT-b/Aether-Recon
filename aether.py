#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import json
from datetime import datetime

# --- Aether Visual Palette (Recon Blue Edition) ---
PRIMARY = '\033[38;5;33m'    # Recon Blue
SECONDARY = '\033[38;5;45m'  # Electric Blue
SUCCESS = '\033[38;5;82m'    # Neon Green
ACCENT = '\033[38;5;202m'    # Status Orange
ERROR = '\033[38;5;196m'     # Red
BOLD = '\033[1m'
RESET = '\033[0m'

def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{PRIMARY}{BOLD}" + "═"*65 + f"\n" + """
█████╗ ███████╗████████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗
███████║█████╗     ██║   ███████║█████╗  ██████╔╝
██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗
██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
         V4.2 | Professional Recon Edition
""" + "═"*65 + f"{RESET}")

def check_dependencies():
    tools = {'nmap': 'nmap --version', 'ffuf': 'ffuf -V', 'whatweb': 'whatweb --version'}
    missing = [t for t, cmd in tools.items() if subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0]
    
    if not missing: return True
    
    print(f"{ERROR}[!] Missing or broken tools: {', '.join(missing)}{RESET}")
    choice = input(f"{ACCENT}[?] Install/Repair them automatically? (Y/n): {RESET}").lower()
    if choice in ['y', 'yes', '']:
        print(f"{ACCENT}[*] Updating system & fixing tools...{RESET}")
        os.system("sudo apt-get update -y")
        for t in missing:
            os.system(f"sudo apt-get install --reinstall -y {t}")
        return True
    return False

def get_next_scan_dir():
    """Finds the next available directory name: Aether_scan_1, 2, etc."""
    counter = 1
    while os.path.exists(f"Aether_scan_{counter}"):
        counter += 1
    return f"Aether_scan_{counter}"

def run_step(step_num, title, command):
    print(f"{PRIMARY}{BOLD}┌──[Step {step_num}/3] {title}{RESET}")
    print(f"{ACCENT}│ Running...{RESET}")
    start = time.time()
    exit_code = os.system(command)
    duration = round(time.time() - start, 2)
    
    if exit_code == 0:
        print(f"{SUCCESS}└─╼ Completed in {duration}s.{RESET}\n")
    else:
        print(f"{ERROR}└─╼ Failed or interrupted after {duration}s.{RESET}\n")

def parse_nmap(file_path):
    ports = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                if "/tcp" in line and "open" in line:
                    ports.append(line.strip())
    return ports

def parse_whatweb(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read().strip()
            return content.split(" [200 OK] ")[-1] if " [200 OK] " in content else content[:100]
    return "No technology data found."

def parse_ffuf(file_path):
    found_paths = []
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for res in data.get('results', []):
                    found_paths.append(f"/{res['input']['FUZZ']} (Status: {res['status']})")
        except: pass
    return found_paths[:10]

def create_smart_report(base_dir, raw_dir, target):
    report_path = f"{base_dir}/Executive_Summary.md"
    ports = parse_nmap(f"{raw_dir}/nmap_scan.txt")
    tech = parse_whatweb(f"{raw_dir}/tech_stack.txt")
    paths = parse_ffuf(f"{raw_dir}/ffuf_results.json")
    
    with open(report_path, 'w') as f:
        f.write(f"# 🛡️ Aether Recon Report: {target}\n")
        f.write(f"**Scan Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 🌐 Network Services\n")
        if ports:
            for p in ports: f.write(f"- `{p}`\n")
        else: f.write("- No open ports found.\n")
        f.write(f"\n> **Quick View:** `cat {raw_dir}/nmap_scan.txt`\n\n")
        f.write("## 🛠️ Technology Stack\n")
        f.write(f"```\n{tech}\n```\n")
        f.write(f"\n> **Quick View:** `cat {raw_dir}/tech_stack.txt`\n\n")
        f.write("## 📂 Top Discovered Paths\n")
        if paths:
            for path in paths: f.write(f"- {path}\n")
        else: f.write("- No interesting paths found.\n")
        f.write(f"\n> **Full JSON Data:** `cat {raw_dir}/ffuf_results.json`\n")

    print(f"{SUCCESS}[+] Smart report generated: {report_path}{RESET}")

def main():
    show_banner()
    if not check_dependencies(): sys.exit(1)
    
    target = input(f"{SECONDARY}{BOLD}» Target Host (e.g. example.com): {RESET}").strip()
    if not target: return

    # Sequential Naming Logic
    base_dir = get_next_scan_dir()
    raw_dir = f"{base_dir}/raw_logs"
    
    os.makedirs(raw_dir, exist_ok=True)
    print(f"{SECONDARY}[ℹ] Session organized in: {base_dir}{RESET}\n")

    full_url = target if target.startswith("http") else f"http://{target}"
    host_clean = target.replace("http://", "").replace("https://", "").split('/')[0]

    # Step 1: Tech Stack
    run_step(1, "Technology Fingerprinting", 
             f"whatweb -a 3 {full_url} --color=never > {raw_dir}/tech_stack.txt")
    
    # Step 2: Nmap
    run_step(2, "Service Discovery", 
             f"nmap -sV -F {host_clean} -oN {raw_dir}/nmap_scan.txt")
    
    # Step 3: FFUF
    wordlist = "/usr/share/wordlists/dirb/common.txt"
    if os.path.exists(wordlist):
        run_step(3, "Path Discovery", 
                 f"ffuf -u {full_url}/FUZZ -w {wordlist} -mc 200,301,302 -t 40 -o {raw_dir}/ffuf_results.json")
    else:
        print(f"{ERROR}[!] Wordlist missing at {wordlist}{RESET}")

    create_smart_report(base_dir, raw_dir, target)
    print(f"\n{PRIMARY}{BOLD}★ Mission Accomplished. Check {base_dir}/Executive_Summary.md ★{RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{ERROR}[!] Execution cancelled by user (Ctrl+C).{RESET}")
        print(f"{ACCENT}[ℹ] Cleaning up... Partial logs might be saved in the session folder.{RESET}")
        sys.exit(0)
