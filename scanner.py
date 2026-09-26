import socket
import threading
from queue import Queue, Empty

# Queue for storing ports and list for storing discovered open ports
queue = Queue()
openPorts = []
lock = threading.Lock()
scanned_count = 0

def get_scan_parameters():
    """
    Prompts the user for target IP and valid port ranges.
    Returns target IP/hostname, start port, and end port.
    """
    while True:
        target = input("Enter target IP address or hostname: ").strip()
        try:
            socket.gethostbyname(target)
            break
        except socket.gaierror:
             print(f"[-] Could not resolve '{target}'. Please enter a valid IP or hostname.\n")

    while True:
        try:
            start_port = int(input("Enter starting port (e.g., 1): "))
            end_port = int(input("Enter ending port (e.g., 1024): "))

            # Validate port boundaries
            if 1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port:
                return target, start_port, end_port
            else:
                print("[-] Invalid range. Ports must be between 1 and 65535, and start port <= end port.\n")
        except ValueError:
            print("[-] Invalid input! Please enter whole numbers for port values.\n")

def portscan(target, port):
    """
    Attempts to establish a TCP connection to a specific port on the target host.
    Returns True if open, False otherwise.
    """
    netSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    netSocket.settimeout(1.0)  # 1-second timeout to prevent hanging

    try:
        netSocket.connect((target, port))
        try:
            netSocket.settimeout(0.5)
            banner = netSocket.recv(1024).decode(errors="ignore").strip()
        except (socket.timeout, OSError):
            banner = ""
        return True, banner
    except (socket.timeout, OSError):
        return False, ""
    finally:
        netSocket.close()

def QS(portlist):
    """Populates the queue with target ports."""
    for port in portlist:
        queue.put(port)

def worker(target):
    """
    Worker function executed by each thread to pull ports from the queue.
    """
    global scanned_count
    while True:
        try:
            # Atomic queue fetch to prevent thread race conditions
            port = queue.get_nowait()
        except Empty:
            break

        is_open, banner = portscan(target, port)
        if is_open:
            if banner:
                print(f"[+] Port {port} is open — {banner}")
            else:
                print(f"[+] Port {port} is open")
            with lock:
                openPorts.append(port)

        with lock:
            scanned_count += 1

        queue.task_done()

if __name__ == "__main__":
    # Collect input parameters from user
    target, start_port, end_port = get_scan_parameters()

    # Creating port list (+1 ensures end_port is included)
    portlist = range(start_port, end_port + 1)
    QS(portlist)
    print(f"\n[*] Starting scan on target {target} across ports {start_port}-{end_port}...")
    thread_count = min(100, len(portlist))

    threadList = []
    for tl in range(thread_count):
        # 'target' as an argument to worker thread
        thread = threading.Thread(target=worker, args=(target,))
        threadList.append(thread)

    for thread in threadList:
        thread.start()

    for thread in threadList:
        thread.join()

    print("\n[*] Scan Complete.")
    print(f"\n[*] Total ports scanned: {scanned_count}")
    print("Open ports are:", sorted(openPorts))

    with open("scan_results.txt", "w") as f:
        f.write(f"Scan target: {target}\n")
        f.write(f"Port range: {start_port}-{end_port}\n")
        f.write("Open ports:\n")
        for port in sorted(openPorts):
            f.write(f"{port}\n")

print(f"\n[*] Results also saved to scan_results.txt")
