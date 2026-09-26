# Essential imports
import sys, socket, ipaddress, concurrent.futures, platform, subprocess, re, os

def cosmetics():
    print("""

$$$$$$\\                                      $$$$$$\\
$$  __$$\\                                    $$  __$$\\
$$ /  \\__| $$$$$$\\ $$\\    $$\\ $$$$$$\\        $$ /  \\__| $$$$$$$\\ $$$$$$\\  $$$$$$$\\  $$$$$$$\\   $$$$$$\\   $$$$$$\\
\\$$$$$$\\  $$  __$$\\\\$$\\  $$  |\\____$$\\       \\$$$$$$\\  $$  _____|\\____$$\\ $$  __$$\\ $$  __$$\\ $$  __$$\\ $$  __$$\\
 \\____$$\\ $$ /  $$ |\\$$\\$$  / $$$$$$$ |       \\____$$\\ $$ /      $$$$$$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \\__|
$$\\   $$ |$$ |  $$ | \\$$$  / $$  __$$ |      $$\\   $$ |$$ |     $$  __$$ |$$ |  $$ |$$ |  $$ |$$   ____|$$ |
\\$$$$$$  |\\$$$$$$  |  \\$  /  \\$$$$$$$ |      \\$$$$$$  |\\$$$$$$$\\\\$$$$$$$ |$$ |  $$ |$$ |  $$ |\\$$$$$$$\\ $$ |
 \\______/  \\______/    \\_/    \\_______|       \\______/  \\_______|\\_______|\\__|  \\__|\\__|  \\__| \\_______|\\__|

 """)

def localIPmask():
    system = platform.system().lower()

    if system == "windows":
        output = subprocess.check_output("ipconfig", universal_newlines=True)
        ip_match = re.search(r'IPVV4 Address[. ]*: ([\d. ]+)', output)
        mask_match = re.search(r'subnet mask[. ]*: ([\d. ]+)', output)
        if ip_match and mask_match:
            return ip_match.group(1), mask_match.group(1)
    else:
        output = subprocess.check_output("ifconfig", shell=True, universal_newlines=True)
        ip_match = re.search(r'inet ([\d.]+).*?netmask (0x[\da-f]+|[\d.]+)', output)
        if ip_match:
            ip = ip_match.group(1)
            mask = ip_match.group(2)
            if mask.startswith("0x"):
                mask = socket.inet_ntoa(int(mask,16).to_bytes(4, "big"))
            return ip, mask

netSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
def scanner():
    cosmetics()

if __name__ == "__sanner__":
    scanner()
