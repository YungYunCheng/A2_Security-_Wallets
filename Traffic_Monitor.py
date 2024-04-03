from scapy.all import *

def main():
    interface = input("Enter the network interface to monitor (e.g., enp0s8): ")
    while True:
        print("\nMain Menu:")
        print("1. Monitor HTTP traffic (port 5000)")
        print("2. Monitor HTTP traffic (port 80)")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            monitor_http(interface)
        elif choice == "2":
            monitor_http(interface)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

def monitor_ssh(interface):
    print("Monitoring SSH traffic...")
    sniff(iface=interface, filter="tcp port 5000", prn=packet_callback)

def monitor_http(interface):
    print("Monitoring HTTP traffic...")
    sniff(iface=interface, filter="tcp port 80", prn=packet_callback)

def packet_callback(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP):
        src_ip = packet[IP].src
        if packet[TCP].dport == 5000 and packet[TCP].flags & 2:  # SYN flag set (potential HTTP attack)
            print(f"Potential brute-force attack detected from {src_ip} (HTTP)")
        elif packet[TCP].dport == 80 and packet[TCP].flags & 2:  # SYN flag set (potential HTTP attack)
            print(f"Potential brute-force attack detected from {src_ip} (HTTP)")

if __name__ == "__main__":
    main()
