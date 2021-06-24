import scapy.all as scapy
import optparse as parse


def get_arguments():
    parser = parse.OptionParser()
    parser.add_option("-i", "--ip", dest="ip", help="IP address of device that you want to get mac address")
    (options, arguments) = parser.parse_args()
    if not options.ip:
        parser.error("[-] Please specify an IP, use --help for more info.")
    return options


def scan(ip):
    ARPrequest = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    package = ARPrequest/broadcast
    answered_list = scapy.srp(package, timeout=1, verbose=False)[0]
    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(result_list):
    print("IP\t\t\tMAC address\n------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])


options = get_arguments()
result_list = scan(options.ip)
print_result(result_list)
