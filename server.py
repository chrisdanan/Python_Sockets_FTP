from socket import *
import os
import sys

#Check the arguments passed by the command line.
if len(sys.argv) != 2:
	print("USAGE python " + sys.argv[0] + " <port_number>")
	sys.exit()

#The port on which to listen.
serverPort = int(sys.argv[1])

#Create a TCP socket.
serverSocket = socket(AF_INET, SOCK_STREAM)

#Bind the socket to the port.
serverSocket.bind(("", serverPort))

#Start listening for incoming connections.
serverSocket.listen(1)

print("The server is ready to receive.")

#Accept incoming connections.
while 1:
	#Accept a connection and get client's socket.
	connectionSocket, addr = serverSocket.accept()

	print("Accepted connection from " + str(addr))

	#Send to the client that the server is ready to receive ftp commands.
	connectionSocket.send("1")

	#Wait for incoming ftp commands.
	while 1:
		print("Waiting for command from client.")

		#Receive a command from the client.
		command = connectionSocket.recv(4)

		#If the command is 'exit', then exit the ftp session.
		if command == "exit":
			print("Command received was 'exit'")
			#Send back a 0 to the client to indicate that the ftp session is over.
			connectionSocket.send("0")
			#Break out of the inner while loop.
			break
		else:
			print("Could not understand; please input another command")
			connectionSocket.send("1")

	print("Closing connection")

	connectionSocket.close()