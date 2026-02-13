#!/usr/bin/env python3
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
    """Displays the interactive CLI banner"""
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
    """Checks for required tools and offers auto-installation if missing"""
    tools = {
        'nmap': 'nmap --version',
        'ffuf': 'ffuf -V',
        'whatweb': 'whatweb --version'
    }
    missing = []
    
    for tool, cmd in tools.items():
        # Checking if tool is installed and functional
        check = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if check.returncode != 0:
            missing.append(tool)
    
    if not missing:
        return True

    print(f"{ERROR}[!] Missing or corrupted dependencies: {', '.join(missing)}{RESET}")
    
    try:
        choice = input(f"{ACCENT}» Install missing tools automatically? (Y/n): {RESET}").strip().lower()
        if choice in ['y', 'yes', '']:
            print(f"{SECONDARY}[ℹ] Updating package lists...{RESET}")
            subprocess.run("sudo apt-get update", shell=True)
            
            for tool in missing:
                print(f"{SECONDARY}[+] Installing {tool}...{RESET}")
                # Reinstalling to fix potential library issues (like WhatWeb Ruby errors)
                install_cmd = f"sudo apt-get install --reinstall -y {tool}"
                result = subprocess.run(install_cmd, shell=True)
                
                if result.returncode != 0:
                    print(f"{ERROR}[!] Failed to install {tool}. Please check your connection.{RESET}")
                    return False
            
            print(f"{SUCCESS}[+] Dependencies resolved!{RESET}\n")
            return True
        else:
            return False
    except KeyboardInterrupt:
        return False

def run_step(step_num, title, command, wait_msg=None):
    """Executes a reconnaissance step and logs duration"""
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
        print(f"{ERROR}└─╼ Task stopped or failed.{RESET}\n")

def create_md_report(folder, target):
    """Generates a final summary report in Markdown format"""
    report_path = f"{folder}/Final_Report.md"
    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Reconnaissance Report: {target}\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## 🛠 Tools Used\n- WhatWeb\n- Nmap\n- FFUF\n\n")
            f.write("## 📝 Summary\n")
            f.write(f"Raw scan results are located in the `{folder}` directory.")
        print(f"{SUCCESS}[+] Final report generated: {report_path}{RESET}")
    except Exception as e:
        print(f"{ERROR}[!] Report generation failed: {e}{RESET}")

def main():
    show_banner()
    
    if not check_dependencies():
        print(f"{ERROR}[!] Execution aborted due to missing tools.{RESET}")
        sys.exit(1)
        
    try:
        raw_target = input(f"{SECONDARY}{BOLD}» Target Host (e.g., example.com): {RESET}").strip()
        if not raw_target:
            print(f"{ERROR}[!] Error: No target provided.{RESET}")
            return

        # Target parsing
        host_only = raw_target.replace("http://", "").replace("https://", "").split('/')[0]
        full_url = raw_target if raw_target.startswith("http") else f"http://{raw_target}"
        full_url = full_url.rstrip('/')

        # Directory setup
        timestamp = datetime.now().strftime("%H%M")
        base_dir = f"Aether_{host_only.replace('.', '_')}_{timestamp}"
        
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            print(f"{SECONDARY}[ℹ] Session logs: {base_dir}{RESET}\n")

        # --- Step 1: Technology Stack (WhatWeb) ---
        run_step(1, "Tech Fingerprinting",
                 f"whatweb -a 3 {full_url} --color=never > {base_dir}/tech_stack.txt",
                 "Identifying web server, CMS, and frameworks...")

        # --- Step 2: Service Enumeration (Nmap) ---
        run_step(2, "Service Discovery",
                 f"nmap -sV -F {host_only} -oN {base_dir}/nmap_scan.txt",
                 "Scanning common ports and service versions...")

        # --- Step 3: Directory Fuzzing (FFUF) ---
        wordlist = "/usr/share/wordlists/dirb/common.txt" 
        if os.path.exists(wordlist):
            run_step(3, "Path Discovery",
                     f"ffuf -u {full_url}/FUZZ -w {wordlist} -mc 200,301,302 -t 40 -o {base_dir}/ffuf_results.json",
                     "Searching for hidden directories...")
        else:
            print(f"{ERROR}[!] Wordlist not found. Skipping FFUF step.{RESET}\n")

        # --- Cleanup & Finalize ---
        create_md_report(base_dir, host_only)
        print(f"\n{ACCENT}{BOLD}★ Mission Accomplished. Results saved to {base_dir} ★{RESET}")

    except KeyboardInterrupt:
        print(f"\n{ERROR}[!] User interrupted. Exiting...{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    main()
