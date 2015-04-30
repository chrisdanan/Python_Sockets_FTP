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

	data = "It works!"

	connectionSocket.send(data)

	connectionSocket.close()