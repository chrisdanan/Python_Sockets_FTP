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

while True:

    #Used to determine if the client is still connected to the server.
    connectionFlag = clientSocket.recv(9)

    #If server gives back connection flag of 1, then send it gives the OK for client to send a command.
    if connectionFlag == "1":
    	#Reference for getting raw input:
    	#http://stackoverflow.com/questions/3345202/python-getting-user-input
    	#User types in a command that will be sent to the server.
    	command = raw_input("ftp>>")

    	#Send the command to the server.
    	clientSocket.send(command)

    	#Receive a new connectionFlag from the server.
    	connectionFlag = clientSocket.recv(9)

    #If the server sends back any other number, then break out of the loop (indicates that server is done accepting commands).
    else:
    	break

print("Finished with client")


    