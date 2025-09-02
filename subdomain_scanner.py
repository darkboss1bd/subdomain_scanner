import requests
import time
import sys
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# ============ BANNER with Hacker Animation ============
def print_banner():
    banner = f"""
{Fore.GREEN}╔════════════════════════════════════════════════╗
{Fore.GREEN}║{Fore.CYAN}  ██████╗  █████╗ ████████╗███████╗ ██████╗ ██╗  ██╗{Fore.GREEN}║
║{Fore.CYAN}  ██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔═══██╗██║ ██╔╝{Fore.GREEN}║
║{Fore.CYAN}  ██████╔╝███████║   ██║   █████╗  ██║   ██║█████╔╝ {Fore.GREEN}║
║{Fore.CYAN}  ██╔══██╗██╔══██║   ██║   ██╔══╝  ██║   ██║██╔═██╗ {Fore.GREEN}║
║{Fore.CYAN}  ██████╔╝██║  ██║   ██║   ███████╗╚██████╔╝██║  ██╗{Fore.GREEN}║
║{Fore.CYAN}  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝{Fore.GREEN}║
{Fore.GREEN}╠════════════════════════════════════════════════╣
{Fore.GREEN}║{Fore.RED}   [>] BATCH SUBDOMAIN FINDER v2.0            {Fore.GREEN}║
{Fore.GREEN}║{Fore.YELLOW}   [>] Coded by: {Fore.MAGENTA}darkboss1bd                   {Fore.GREEN}║
{Fore.GREEN}╚════════════════════════════════════════════════╝
    """
    for line in banner.split('\n'):
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.005)
        print()

# ============ Loading Animation ============
def loading(text, duration=2):
    print(Fore.CYAN + text, end="")
    for _ in range(duration * 5):
        sys.stdout.write(Fore.YELLOW + "█")
        sys.stdout.flush()
        time.sleep(0.1)
    print(Fore.GREEN + " DONE!")

# ============ Read subdomain wordlist ============
def load_wordlist(file_path="subdomains.txt"):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(Fore.RED + f"[-] Wordlist not found: {file_path}")
        sys.exit(1)

# ============ Scan single domain ============
def scan_domain(domain, wordlist):
    found = []
    domain = domain.strip().lower().replace("https://", "").replace("http://", "").split("/")[0]
    print(Fore.WHITE + f"\n[+] Scanning: {Fore.YELLOW}{domain}")

    total = len(wordlist)
    for idx, sub in enumerate(wordlist):
        url = f"https://{sub}.{domain}"
        try:
            response = requests.get(url, timeout=3, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code in [200, 301, 302, 403]:
                print(Fore.GREEN + f"  [FOUND] {url} [{response.status_code}]")
                found.append(f"{url} [{response.status_code}]")
        except:
            pass

        # Progress
        if (idx + 1) % 50 == 0 or idx == total - 1:
            progress = (idx + 1) / total * 100
            print(Fore.BLUE + f"  └─ Progress: {idx + 1}/{total} ({progress:.1f}%)", end="\r")

    print(Fore.MAGENTA + f"\n  [✓] Found {len(found)} subdomains for {domain}")
    return found

# ============ Save results to file ============
def save_results(results_dict):
    filename = f"batch_scan_results_{int(time.time())}.txt"
    with open(filename, 'w') as f:
        f.write("===== BATCH SUBDOMAIN SCAN RESULTS =====\n")
        f.write("Coded by: darkboss1bd\n")
        f.write("Tool: Advanced Batch Subdomain Finder\n")
        f.write("="*50 + "\n\n")
        for domain, results in results_dict.items():
            f.write(f"[DOMAIN] {domain}\n")
            if results:
                for r in results:
                    f.write(f"  → {r}\n")
            else:
                f.write("  → No subdomains found.\n")
            f.write("\n")
    print(Fore.GREEN + f"\n[✓] All results saved to: {filename}")

# ============ Main Function ============
def main():
    print_banner()
    loading("[*] Loading darkboss1bd's Batch Subdomain Scanner", 2)
    
    wordlist = load_wordlist()
    print(Fore.CYAN + f"[✓] Loaded {len(wordlist)} subdomain patterns.")

    print(Fore.WHITE + "\n[?] Enter domains (one per line). Press Enter twice to start:")
    domains = []
    while True:
        try:
            domain = input(Fore.YELLOW + "Domain: ").strip()
            if not domain:
                break
            # Clean domain
            domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
            if domain and domain.count('.') >= 1:
                domains.append(domain)
            else:
                print(Fore.RED + "  [!] Invalid domain format, skipping...")
        except KeyboardInterrupt:
            break

    if not domains:
        print(Fore.RED + "[-] No domains entered. Exiting...")
        return

    print(Fore.MAGENTA + f"\n[✓] Starting batch scan for {len(domains)} domains...\n")
    results = {}

    for domain in domains:
        found = scan_domain(domain, wordlist)
        results[domain] = found
        time.sleep(0.5)  # Small delay

    # Save all results
    save_results(results)
    print(Fore.GREEN + "\n[✓] Batch scanning completed. Stay dark, stay powerful. — darkboss1bd")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[!] Scan interrupted by user. Exiting gracefully...")
    except Exception as e:
        print(Fore.RED + f"[-] Unexpected error: {e}")