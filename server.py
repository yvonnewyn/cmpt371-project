# Include Python's Socket Library
from socket import *

# Specify Server Port
# serverHost = 'localhost'
serverHost = ''

serverPort = 8000

# Create TCP welcoming socket
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.settimeout(10)

# Bind the server port to the socket
serverSocket.bind((serverHost,serverPort))

# Server begins listerning foor incoming TCP connections
serverSocket.listen(1)
print ('Listening on port ', serverPort, '...')

while True: # Loop forever
    # Server waits on accept for incoming requests.
    # New socket created on return
    try:
        connectionSocket, addr = serverSocket.accept()
    except timeout:
        continue

    # Read from socket (but not address as in UDP)
    request = connectionSocket.recv(1024).decode()
    print(request)

    if (request==''):
        reply = 'HTTP/1.0 408 Request Timed Out\n\n408 Request Timed Out'

    else:
        # Get HTTP header
        header = request.split('\n')    
        filename = header[0].split()[1]

        if (filename == '/'):
            filename = 'test.html'
        else:
            filename = filename[1:]

        try:
            f = open(filename)
            content = f.read()
            f.close()

            reply = 'HTTP/1.0 200 OK\n\n' + content

        except FileNotFoundError:
            reply = 'HTTP/1.0 404 Not Found\n\n404 Not Found'

        # Send the reply
        try:
            connectionSocket.sendall(reply.encode())

        except timeout:
            reply = 'HTTP/1.0 408 Request Timed Out\n\n408 Request Timed Out'

    # Close connection to client (but not welcoming socket)
    connectionSocket.close()

serverSocket.close()