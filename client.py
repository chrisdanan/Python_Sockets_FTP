# Client code

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

from socket import *
import os
import sys
import os.path


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

# Check the arguments passed by command line.
if len(sys.argv) != 3:
    print("USAGE python" + sys.argv[0] + " <server_machine> <server_port>")
    sys.exit()

# Server address.
serverAddress = sys.argv[1]

# Server port number.
serverPort = int(sys.argv[2])

# Create a TCP socket.
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to the server.
clientSocket.connect((serverAddress, serverPort))

while True:

    # Used to determine if the client is still connected to the server.
    connectionFlag = clientSocket.recv(9)

    # If server gives back connection flag of 1, then send it gives the OK for client to send a command.
    while connectionFlag == "1":
        # Reference for getting raw input:
        # http://stackoverflow.com/questions/3345202/python-getting-user-input
        # User types in a command that will be sent to the server.
        command = raw_input("ftp> ").split(" ")
            
        if command[0] == "ls":

            #Declare variables
            sData = ""
            recvBuff = ""
            sSize = 0
            sSizeBuff = ""

            #Consider opening an ephemeral port on this one.
            clientSocket.send(command[0])

            #Generate the ephemeral port.
            #Reference: Professor Gofman's code.
            dataSocket = socket(AF_INET, SOCK_STREAM)
            dataSocket.bind(("", 0))
            print("I chose ephemeral port: ", dataSocket.getsockname()[1])

            #Send ephemeral port number to the server.
            clientSocket.send(str(dataSocket.getsockname()[1]))
            dataSocket.listen(1)

            while 1:
                print("Waiting for server connection to data channel")

                #Accept connection from the server.
                connectionSocket, addr = dataSocket.accept()

                print("Received connection from server.")

                #Get the size of the incoming data from the server.
                sSizeBuff = recvAll(connectionSocket, 10)

                sSize = int(sSizeBuff)

                #Get the data from the server (get the list of files on the server)
                #NOTE: Since we are using localhost as our client and server, this should be the same list as 'lls'.
                sData = recvAll(connectionSocket, sSize)

                #Print the data to the client.
                print("Data received from the server:")
                print(sData)
                print("Size of data: ", sSize)

                #Get connectionFlag from server.
                connectionFlag = clientSocket.recv(9)

                #Close the data connection.
                connectionSocket.close()

                break

        elif command[0] == "lls":
            # Get the real path of this file we are running. 
            path = os.path.dirname(os.path.realpath(__file__))
            # Get the list of files in the directory.
            lls = os.listdir(path)
            # Print the list
            for value in lls:
                print (value)
        elif command[0] == "get":
            if len(command) !=2:
                print("USAGE get <filename>")
            else:

                #Send 'get' command.
                clientSocket.send(command[0])

                #Send filename.
                clientSocket.send(command[1])

                fileExistsFlag = clientSocket.recv(9)

                print("fileExistsFlag", fileExistsFlag)

                if fileExistsFlag == "1":
                    #Generate ephemeral port.
                    #Reference: Professor Gofman's example code.
                    dataSocket = socket(AF_INET, SOCK_STREAM)
                    dataSocket.bind(("", 0))
                    print("I chose ephemeral port: ", dataSocket.getsockname()[1])

                    #Send ephemeral port number to server.
                    clientSocket.send(str(dataSocket.getsockname()[1]))
                    dataSocket.listen(1)

                    while 1:
                        print("Waiting for server connection to channel.")
                        connectionSocket, addr = dataSocket.accept()

                        print("Received connection from the server.")

                        #The buffer to all data received from the server.
                        fileData = ""

                        #The size of the incoming file.
                        recvBuff = ""

                        fileSize = 0
                        #The buffer containing the file size.
                        fileSizeBuff = ""

                        #Receive the first 10 bytes indicating the size of the file.
                        fileSizeBuff = recvAll(connectionSocket, 10)

                        fileSize = int(fileSizeBuff)

                        print("The file size is ", fileSize)

                        #Get the file data.
                        fileData = recvAll(connectionSocket, fileSize)

                        print (fileData)

                        print("File received: " + command[1])
                        print("Size of file received: ", fileSize)

                        print("Saving data to a file")

                        solutionFile = open('client_received.txt', 'w')
                        solutionFile.write(fileData)
                        solutionFile.close()

                        connectionSocket.close()

                        break
                else:
                    print("Server does not have that file.")
                    connectionFlag = "1"

        elif command[0] == "put":
            #Check for correct usage of 'put'
            if len(command) != 2:
                print("USAGE put <filename>")
            else:
                #Store filename into a variable.
                fileName = command[1]

                path = os.path.dirname(os.path.realpath(__file__))
                
                #Send the file to the server if it exists.
                #Reference: http://stackoverflow.com/questions/82831/check-if-a-file-exists-using-python#comment38282943_82852
                if os.path.isfile(path + "/" + fileName) == True:

                    #Open the file.
                    fileObj = open(fileName, "r")

                    #The file data.
                    fileData = None

                    # Send 'put' command to server.
                    clientSocket.send(command[0])

                    #Generate ephemeral port.
                    #Reference: Professor Gofman's example code.
                    dataSocket = socket(AF_INET, SOCK_STREAM)
                    dataSocket.bind(("", 0))
                    print("I chose ephemeral port: ", dataSocket.getsockname()[1])

                    #Send ephemeral port number to server.
                    clientSocket.send(str(dataSocket.getsockname()[1]))

                    dataSocket.listen(1)

                    while 1:
                        print("Waiting for server connection to data channel.")

                        connectionSocket, addr = dataSocket.accept()

                        print("Received connection from the server.")

                        #Read 65536 bytes of data.
                        fileData = fileObj.read(65536)

                        #Make sure we did not hit EOF.
                        if fileData:

                            #Get the size of the data read and convert it to string.
                            dataSizeStr = str(len(fileData))

                            #Prepend 0's to the size string until the size is 10 bytes.
                            while len(dataSizeStr) < 10:
                                dataSizeStr = "0" + dataSizeStr

                            #Prepend the size of the data to the file data.
                            fileData = dataSizeStr + fileData

                            #The number of bytes sent.
                            numSent = 0

                            #Send the data!
                            while len(fileData) > numSent:
                                numSent += connectionSocket.send(fileData[numSent:])

                            #At this point, the client is done sending file data to the server.

                            #Print out file name and number of bytes transferred.
                            print("Sent " + fileName + " to the server.")
                            print(numSent, " bytes sent to the server.")

                            #Finished sending the data, so close the data connection.
                            connectionSocket.close()

                            #Get the connection flag from the server.
                            connectionFlag = clientSocket.recv(9)
                            break
                else:
                    print("File does not exist")

        elif command[0] == "quit":
            # Send the command to the server.
            clientSocket.send(command[0])
            # Receive a new connectionFlag from the server.
            connectionFlag = clientSocket.recv(9)
            break
        elif command[0] == "":
            # If blank, do nothing.
            pass
        else:
            # If wrong command, print this and do nothing afterward.
            print("Invalid command entered.")


    # If the server sends back any other number, then break out of the loop (indicates that server is done accepting commands).
    break

# If we break from the loops the application will close.
clientSocket.close()
print("Finished with client")
print("Closing connection")


    