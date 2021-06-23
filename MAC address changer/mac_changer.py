import subprocess as sp
import optparse as parse
import re



def get_arguments():
    parser = parse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
    parser.add_option("-m", "--mac", dest="newMac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.newMac:
        parser.error("[-] Please specify a new MAC address, use --help for more info.")
    return options

def change_mac(interface, newMac):
    print("[+] Changing MAC address for " + interface + " to " + newMac)
    sp.call("ifconfig " + interface + " down", shell=True)
    sp.call("ifconfig " + interface + " hw ether " + newMac, shell=True)
    sp.call("ifconfig " + interface + " up", shell=True)

def cur_mac(interface):
    ifconfigResult = sp.check_output(["ifconfig", interface])
    if ifconfigResult:
        MACSearch = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfigResult))
        if MACSearch:
            return MACSearch.group(0)
    else:
        print("[-] Could not found MAC address.")


option = get_arguments()
oldMac = cur_mac(option.interface)
print("Current MAC =", str(oldMac))
change_mac(option.interface,option.newMac)
if str(cur_mac(option.interface)) != option.newMac:
    print("[-] Something went wrong. Old MAC address equal new MAC address")
else:
    print("[+] Changing was successfully! Current MAC =", cur_mac(option.interface))
