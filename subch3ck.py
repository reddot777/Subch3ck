import requests
from concurrent.futures import ThreadPoolExecutor
import time
from colorama import Fore, init

init(autoreset=True)

path = input(f"{Fore.YELLOW}Enter path : ")
valid_subdomains_path = "valid_subdomains.txt"

def scan_subdomain(thread):
    thread = thread.strip()

    if not thread.startswith("http://") and not thread.startswith("https://"):
        thread = "http://" + thread

    try:
        response = requests.get(thread, timeout=5)
        st = response.status_code

        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] {thread} ====> 200 [VALID]{Fore.RESET}")
            save_valid_subdomain(thread)
        else:
            print(f"{Fore.RED}[-] {thread} ====> {st} [INVALID]{Fore.RESET}")

    except requests.RequestException as e:
        print(f"{Fore.RED}[-] {thread} ====> Error or 404 [INVALID]{Fore.RESET}")

def save_valid_subdomain(subdomain):
    with open(valid_subdomains_path, "a") as file:
        file.write(subdomain + "\n")

def main():
    with open(path, "r") as file:
        lines = file.readlines()

    total = len(lines)

    ascii = r"""
     _______. __    __  .______     ______  __    __   ____     ______  __  ___
    /       ||  |  |  | |   _  \   /      ||  |  |  | |___ \   /      ||  |/  /
   |   (----`|  |  |  | |  |_)  | |  ,----'|  |__|  |   __) | |  ,----'|  '  /
    \   \    |  |  |  | |   _  <  |  |     |   __   |  |__ <  |  |     |    <
.----)   |   |  `--'  | |  |_)  | |  `----.|  |  |  |  ___) | |  `----.|  .  \
|_______/     \______/  |______/   \______||__|  |__| |____/   \______||__|\__\

               Coded by @reddot777
               Github : https://github.com/reddot777
    """

    print(f"{Fore.YELLOW}" + ascii + f"{Fore.RESET}")

    print(f"{Fore.YELLOW}==================================")
    print(f"{Fore.YELLOW}{total} subdomains to scan...")
    print(f"{Fore.YELLOW}==================================")

    with open(valid_subdomains_path, "w") as file:
        file.truncate(0)

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(scan_subdomain, lines)

    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}==================================")
        print(f"{Fore.YELLOW}Scan interrupted by user.")
        print(f"{Fore.YELLOW}Valid Domains have been saved in {valid_subdomains_path}.")
        print(f"{Fore.YELLOW}==================================")

    else:
        print(f"{Fore.YELLOW}==================================")
        print(f"{Fore.YELLOW}Scan Status: Finished")
        print(f"{Fore.YELLOW}Valid Domains have been saved in {valid_subdomains_path}.")
        print(f"{Fore.YELLOW}==================================")

if __name__ == "__main__":
    main()
