# Include Python's Socket Library
from socket import *

# Specify Server Address
serverName = 'localhost'
serverPort = 8001
# serverPort = 8001

date = "Wed, 30 Nov 2022 09:55:23"
request = f"GET / HTTP/1.1\r\nHost: localhost:8001\r\n"
# request = f"GET / HTTP/1.1\r\nHost: localhost:8001\r\nIf-Modified-Since: " + date



# Create TCP Socket for Client
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connect to TCP Server Socket
clientSocket.connect((serverName,serverPort))



# Send! No need to specify Server Name and Server Port! Why?
clientSocket.send(request.encode())

# Read reply characters! No need to read address! Why?
response = clientSocket.recv(1024)

# Print out the received string
print ('From Server:', response.decode())

# Close the socket
clientSocket.close()
