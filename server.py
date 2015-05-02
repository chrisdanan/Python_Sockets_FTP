from socket import *
import os
import sys

#Authors:
#   Mario Andrade
#   Christopher Dancarlo Danan
#   Austin Greene
#   Sarah Lee
#For:
#   CPSC 471
#   Assignment 3
#Due:
#   May 1, 2015
#References:
#   Professor Gofman's sample codes from Titanium.

#Reference: Professor Gofman's sample code.
# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff

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

		#If the command is 'quit', then quit the ftp session.
		if command == "quit":
			print("Command received was 'quit'")
			#Send back a 0 to the client to indicate that the ftp session is over.
			connectionSocket.send("0")
			#Break out of the inner while loop.
			break
		elif command == "ls":
			print("ls: print the list of files")

			#Receive ephemeral port from client.
			ephemeralPort = int(connectionSocket.recv(10))
			print("Received ephemeral port: ", ephemeralPort)

			#Create new data connection for data transfer.
			serverDataSocket = socket(AF_INET, SOCK_STREAM)
			serverDataSocket.connect(("localhost", ephemeralPort))

			s = ""

			#Get the real path of this file we are running.
			path = os.path.dirname(os.path.realpath(__file__))

			#Get the list of files in the directory.
			ls = os.listdir(path)

			#Attach all the file names to s.
			for value in ls:
				s = s + value + "\n"

			#Get the size of the data read and convert it to string.
			size = str(len(s))

			#Pad size with 0s to make a 10 byte header.
			while len(size) < 10:
				size = "0" + size

			#Put size in front of data.
			s = size + s

			#Number of bytes sent.
			numSent = 0

			#Send the data (list of files on the server)
			while len(s) > numSent:
				numSent += serverDataSocket.send(s[numSent:])

			print("SUCCESS")

			#Close the data connection.
			serverDataSocket.close()

			connectionSocket.send("1")
		#If the command is 'put', then client wants to put a file onto the server.
		elif command == "put":
			print("Command received was 'put'")

			#Receive ephemeral port from client.
			serverEphemeralPort = int(connectionSocket.recv(10))
			print("Received ephemeral port: ", serverEphemeralPort)

			#Create new data connection for data transfer
			serverDataSocket =socket(AF_INET, SOCK_STREAM)
			serverDataSocket.connect(("localhost", serverEphemeralPort))

			#The buffer to all data received from the client.
			fileData = ""

			#The temporary buffer to store the received data.
			recvBuff = ""

			#The size of the incoming file.
			fileSize = 0

			#The buffer containing the file size.
			fileSizeBuff = ""

			#Receive the first 10 bytes indicating the size of the file.
			fileSizeBuff = recvAll(serverDataSocket, 10)

			#Get the file size.
			fileSize = int(fileSizeBuff)

			print("The file size is ", fileSize)

			#Get the file data.
			fileData = recvAll(serverDataSocket, fileSize)

			print("The file data is:" )
			print fileData
			print("Saving data to a file")

			solutionFile = open('received.txt', 'w')
			solutionFile.write(fileData)
			solutionFile.close
			
			serverDataSocket.close()

			print("SUCCESS")

			#Send flag to client indicating that the server is ready to receive more commands.
			connectionSocket.send("1")

		elif command == 'get':
			print('The command received was get')
			fileName = connectionSocket.recv(50)
			print("Waiting for command from client")
			path = os.path.dirname(os.path.realpath(__file__))
			print("Filename is " + fileName)

			#Send the file to the server if it exists.
			#Reference: http://stackoverflow.com/questions/82831/check-if-a-file-exists-using-python#comment38282943_82852
			if os.path.isfile(path + '/' + fileName) == True:

				connectionSocket.send("1")

				#Open the file.
				fileObj = open(fileName, "r")

				#The file data.
				fileData = None

				#Receive ephemeral port from client.
				serverEphemeralPort = int(connectionSocket.recv(10))
				print("Received ephemeral port: ", serverEphemeralPort)

				serverDataSocket = socket(AF_INET, SOCK_STREAM)
				serverDataSocket.connect(("localhost", serverEphemeralPort))

				fileData = fileObj.read(65536)

				if fileData:

					dataSizeStr = str(len(fileData))

					while len(dataSizeStr) < 10:
						dataSizeStr = "0" + dataSizeStr

					fileData = dataSizeStr + fileData

					numSent = 0

					while len(fileData) > numSent:
						numSent += serverDataSocket.send(fileData[numSent:])

					print("Sent " + fileName + " to the client.")
					print(numSent, " bytes sent to the client.")

					connectionSocket.send("1")

					serverDataSocket.close()
			else:
				print("File does not exist")
				connectionSocket.send("0")
	break

connectionSocket.close()
print("Closing connection")

