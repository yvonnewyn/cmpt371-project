# Include Python's Socket Library
from socket import *

def getfile(filename):
    f = getfile_cache(filename)

    if f:
        print(filename, " in cache")
        return f

    else:
        print(filename, " not in cache")
        f = getfile_server(filename)

        if f:
            save_to_cache(filename, f)
            return filename
        else:
            print(filename, " doesn't exist")
            return None

def getfile_cache(filename):
    try:
        f = open('cache/' + filename)
        content = f.read()
        f.close()
        return content

    except FileNotFoundError:
        return None

def getfile_server(filename):
    try:
        response = urlopen(Request('http://localhost:8000' + '/' + filename))
        content = response.read().decode('utf-8')
        return content
    except HTTPError:
        return None
    
def save_to_cache(filename, content):
    print("saving ", filename, " to cache")

    


def main():
    serverHost = ''
    serverPort = 8001

    # Create TCP welcoming socket
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.settimeout(10)

    # Bind the server port to the socket
    serverSocket.bind((serverHost,serverPort))

    # Server begins listerning foor incoming TCP connections
    serverSocket.listen(1) # change 1 to bigger number so connections are able to be queued up
    print ('Proxy server is listening on port ', serverPort, '...')

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
            reply = 'HTTP/1.1 408 Request Timed Out\n\n408 Request Timed Out'

        else:
            # Get HTTP header
            header = request.split('\n')
            method = header[0].split()[0]    
            filename = header[0].split()[1]

            if (filename == '/'):
                filename = 'test.html'
            else:
                filename = filename[1:]

            try:
                content = getfile(filename)

                # reply = 'HTTP/1.0 200 OK\n\n' + content

                reply = struct.pack()

            except FileNotFoundError:
                reply = 'HTTP/1.1 404 Not Found\n\n404 Not Found'

            # Send the reply
            try:
                connectionSocket.sendall(reply.encode())

            except timeout:
                reply = 'HTTP/1.1 408 Request Timed Out\n\n408 Request Timed Out'

        # Close connection to client (but not welcoming socket)
        connectionSocket.close()

    serverSocket.close()