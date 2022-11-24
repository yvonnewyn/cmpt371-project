# Include Python's Socket Library
from socket import *

# Specify Server Port
serverHost = 'localhost'
serverPort = 8000

# Create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Bind the server port to the socket
serverSocket.bind((serverHost,serverPort))

# Server begins listerning foor incoming TCP connections
serverSocket.listen(1)
print ('Listening on port ', serverPort, '...')

while True: # Loop forever
    # Server waits on accept for incoming requests.
    # New socket created on return
    connectionSocket, addr = serverSocket.accept()
     
    # Read from socket (but not address as in UDP)
    request = connectionSocket.recv(1024).decode()
    print(request)
    if (request==''):
        continue

    # Get HTTP header
    header = request.split('\n')    
    filename = header[0].split()[1]
    

    if (filename == '/'):
        filename = 'test.html'

    try:
        f = open(filename)
        content = f.read()
        f.close()

        reply = 'HTTP/1.0 200 OK\n\n' + content

    except FileNotFoundError:
        reply = 'HTTP/1.0 404 NOT FOUND\n\n404 File not found'


    # Send the reply
    connectionSocket.sendall(reply.encode())
     
    # Close connectiion to client (but not welcoming socket)
    connectionSocket.close()

serverSocket.close()
