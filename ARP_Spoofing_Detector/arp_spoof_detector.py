import scapy.all as scapy

#  По IP возвращает Mac
def get_MAC(ip):
    ARPrequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    package = ARPrequest/broadcast
    answered_list = scapy.srp(package, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_MAC(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                print("[+] You are under attack !!!")
        except IndexError:
            pass


sniff("wlan0")