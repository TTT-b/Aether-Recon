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
         V5.0 | Professional Edition
""" + "═"*65 + f"{RESET}")

def check_dependencies():
    """Check for required system binaries"""
    tools = ['nmap', 'ffuf', 'whatweb']
    missing = [t for t in tools if shutil.which(t) is None]
            
    if not missing:
        return True
        
    print(f"{ERROR}[!] Missing dependencies: {', '.join(missing)}{RESET}")
    choice = input(f"{ACCENT}[?] Attempt auto-install via APT? (Y/n): {RESET}").lower()
    if choice in ['y', '']:
        os.system("sudo apt-get update -y && sudo apt-get install -y " + " ".join(missing))
        return all(shutil.which(t) is not None for t in tools)
    return False

def is_resolvable(host):
    """Verify if the target host is reachable via DNS"""
    try:
        socket.gethostbyname(host)
        return True
    except socket.gaierror:
        return False

def get_next_scan_dir():
    """Generate a sequential directory name"""
    counter = 1
    while os.path.exists(f"Aether_scan_{counter}"):
        counter += 1
    return f"Aether_scan_{counter}"

def run_step(step_num, title, command, timeout=300):
    """Execute a scan step with standardized output"""
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

def main():
    show_banner()
    
    # 1. Dependency Validation
    if not check_dependencies(): 
        print(f"{ERROR}[!] Critical dependencies missing. Technical abort.{RESET}")
        sys.exit(1)
    
    # 2. Target Input and Sanitization
    raw_input = input(f"{SECONDARY}{BOLD}» Target Host: {RESET}").strip()
    if not raw_input: return

    # Cleaning input
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
