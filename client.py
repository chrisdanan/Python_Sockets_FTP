#Client code

from socket import *
import os
import sys

#Check the arguments passed by command line.
if len(sys.argv) != 3:
	print("USAGE python" + sys.argv[0] + " <server_machine> <server_port>")
	sys.exit()

#Server address.
serverAddress = sys.argv[1]

#Server port number.
serverPort = int(sys.argv[2])

#Create a TCP socket.
clientSocket = socket(AF_INET, SOCK_STREAM)

#Connect to the server.
clientSocket.connect((serverAddress, serverPort))

testStr = clientSocket.recv(9)

print(testStr)