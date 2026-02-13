import os
import sys
import time
import subprocess
from datetime import datetime

# --- Aether Visual Palette ---
PRIMARY = '\033[38;5;129m'   # Deep Purple
SECONDARY = '\033[38;5;45m'  # Electric Blue
SUCCESS = '\033[38;5;82m'    # Neon Green
ACCENT = '\033[38;5;202m'    # Bright Orange
ERROR = '\033[38;5;196m'     # Red
BOLD = '\033[1m'
RESET = '\033[0m'

def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{PRIMARY}{BOLD}" + "═"*65)
    print(f"""
█████╗ ███████╗████████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗
███████║█████╗     ██║   ███████║█████╗  ██████╔╝
██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗
██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
         V3.5 | Advanced Recon Suite
""")
    print("═"*65 + f"{RESET}")
    print(f"{SECONDARY}[ℹ] Framework: Modular Reconnaissance{RESET}")
    print(f"{SECONDARY}[ℹ] Strategy: Passive Fingerprinting & Path Discovery{RESET}\n")

def check_dependencies():
    tools = ['nmap', 'ffuf', 'whatweb']
    missing = []
    for tool in tools:
        if subprocess.call(f"which {tool}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            missing.append(tool)
    
    if missing:
        print(f"{ERROR}[!] Missing dependencies: {', '.join(missing)}{RESET}")
        print(f"{SECONDARY}[ℹ] Please install them: sudo apt install {' '.join(missing)}{RESET}\n")
        return False
    return True

def run_step(step_num, title, command, wait_msg=None):
    print(f"{PRIMARY}{BOLD}┌──[Step {step_num}/3] {title}{RESET}")
    if wait_msg:
        print(f"{SECONDARY}│ {wait_msg}{RESET}")
    print(f"{SECONDARY}│ Executing: {command}{RESET}")
    
    start_time = time.time()
    exit_code = os.system(command)
    duration = round(time.time() - start_time, 2)
    
    if exit_code == 0:
        print(f"{SUCCESS}└─╼ Completed in {duration}s.{RESET}\n")
    else:
        print(f"{ERROR}└─╼ Task failed or stopped by user.{RESET}\n")

def create_md_report(folder, target):
    report_path = f"{folder}/Final_Report.md"
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Reconnaissance Report: {target}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## 🛠 Tools Inventory\n")
            f.write("- WhatWeb (Passive Fingerprinting)\n")
            f.write("- Nmap (Service Enumeration)\n")
            f.write("- FFUF (Directory Fuzzing)\n\n")
            f.write("## 📝 Scan Summary\n")
            f.write(f"All raw data logs are stored within the `{folder}` directory.\n")
        print(f"{SUCCESS}[+] Report generated: {report_path}{RESET}")
    except Exception as e:
        print(f"{ERROR}[!] Failed to generate report: {e}{RESET}")

def main():
    show_banner()
    if not check_dependencies():
        sys.exit(1)
        
    try:
        raw_target = input(f"{SECONDARY}{BOLD}» Target Host (e.g., example.com): {RESET}").strip()
        if not raw_target:
            print(f"{ERROR}[!] Error: No target provided.{RESET}")
            return

        # URL Parsing
        host_only = raw_target.replace("http://", "").replace("https://", "").split('/')[0]
        full_url = raw_target if raw_target.startswith("http") else f"http://{raw_target}"
        full_url = full_url.rstrip('/')

        timestamp = datetime.now().strftime("%H%M")
        base_dir = f"Aether_{host_only.replace('.', '_')}_{timestamp}"
        
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            print(f"{SECONDARY}[ℹ] Created session directory: {base_dir}{RESET}\n")

        # --- Step 1: Technology Stack ---
        run_step(1, "Technology Fingerprinting",
                 f"whatweb -a 3 {full_url} --color=never > {base_dir}/tech_stack.txt",
                 "Identifying CMS and Frameworks...")

        # --- Step 2: Service Enumeration ---
        run_step(2, "Service Discovery",
                 f"nmap -sV -F {host_only} -oN {base_dir}/nmap_scan.txt",
                 "Scanning Top 100 ports...")

        # --- Step 3: Directory Fuzzing ---
        # שינינו לנתיב הסטנדרטי של קאלי
        wordlist = "/usr/share/wordlists/dirb/common.txt" 
        if os.path.exists(wordlist):
            run_step(3, "Directory Fuzzing",
                     f"ffuf -u {full_url}/FUZZ -w {wordlist} -mc 200,301,302 -t 50 -o {base_dir}/ffuf_results.json",
                     "Hunting for hidden paths...")
        else:
            print(f"{ERROR}[!] Wordlist not found at {wordlist}. Install wordlists or edit path.{RESET}\n")

        # --- Finish ---
        create_md_report(base_dir, host_only)
        print(f"{ACCENT}{BOLD}★ Mission Accomplished. Happy Hacking! ★{RESET}")

    except KeyboardInterrupt:
        print(f"\n{ERROR}[!] Interrupted by user.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
