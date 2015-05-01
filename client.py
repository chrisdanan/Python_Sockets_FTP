# Client code

from socket import *
import os
import sys

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
            #Consider opening an ephemeral port on this one.
            clientSocket.send(command[0])
        elif command[0] == "lls":
            # Get the real path of this file we are running. 
            path = os.path.dirname(os.path.realpath(__file__))
            # Get the list of files in the directory.
            lls = os.listdir(path)
            # Print the list
            for value in lls:
                print (value)
        elif command[0] == "get":
            pass
        elif command[0] == "push":
            pass
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


    