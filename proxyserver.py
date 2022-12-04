# Include Python's Socket Library
from socket import *
from urllib.request import Request, urlopen, HTTPError
import pathlib
import datetime

class BadRequest(Exception):
    pass

def getfile(filename):
    f = getfile_cache(filename)

    if f:
        print(filename, "in cache")
        return f

    else:
        print(filename, "not in cache")
        f = getfile_server(filename)

        if f:
            save_to_cache(filename, f)
            return f
        else:
            print(filename, "doesn't exist")
            return None

def getfile_cache(filename):
    try:
        # firs
        f = open('cache/' + filename)
        content = f.read()
        f.close()
        return content

    except FileNotFoundError:
        return None

def conditionalget(filename, date):
    serverName = 'localhost'
    serverPort = 8000
    try:
        request = f"GET / HTTP/1.1\r\nHost: localhost:8001\r\nIf-Modified-Since: " + date
        # Create TCP Socket for Client
        clientSocket = socket(AF_INET, SOCK_STREAM)

        # Connect to TCP Server Socket
        clientSocket.connect((serverName,serverPort))

        clientSocket.sendall(request.encode())

        response = clientSocket.recv(1024)

        clientSocket.close()

        print(response.decode())

        return response.decode()
        
        

    except FileNotFoundError:
        return None
    except HTTPError:
        return None


def getfile_server(filename):
    try:
        response = urlopen(Request('http://localhost:8000' + '/' + filename))
        content = response.read().decode('utf-8')
        return content
    except HTTPError:
        return None
    
def save_to_cache(filename, content):
    f = open('cache/' + filename, 'w')
    f.write(content)
    f.close()
    print("saving ", filename, " to cache")

def request_info(request):
    # valid_requests = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE']
    conditional_get = False
    date = ''
    header = request.split('\n')

    for h in header:
        if 'If-Modified-Since:' in h.split():
            conditional_get = True
            date = h.split()[1:]
            date = ' '.join(date)

            

    if 'HTTP' in header[0]:
        method = header[0].split()[0]    
        filename = header[0].split()[1]
        # version = header[0].split()[2]

        # if method in valid_requests:
        if method == 'GET':
            return filename, conditional_get, date

        else:
            raise BadRequest("Invalid request")
    else:
        raise BadRequest("Not HTTP")
    
def main():
    serverHost = ''
    serverPort = 8001

    # Create TCP welcoming socket
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # serverSocket.settimeout(30)

    # Bind the server port to the socket
    serverSocket.bind((serverHost,serverPort))

    # Server begins listerning foor incoming TCP connections
    serverSocket.listen(1) # change 1 to bigger number so connections are able to be queued up
    print ('Proxy server is listening on port ', serverPort, '...')

    while True: # Loop forever
        # Server waits on accept for incoming requests.
        # New socket created on return
        connectionSocket, addr = serverSocket.accept()

        try:
            # Read from socket
            request = connectionSocket.recv(1024).decode()
            print(request)

            if (request==''):
                print('no request')
                reply = 'HTTP/1.1 408 Request Timed Out\n\n408 Request Timed Out'

            else:
                filename, c_get, date = request_info(request)

                if (filename == '/'):
                    filename = 'test.html'
                else:
                    filename = filename[1:]

                content = getfile(filename)

                if c_get:
                    reply = conditionalget(filename, date)
                elif content:
                    reply = 'HTTP/1.1 200 OK\n\n' + content
                else:
                    reply = 'HTTP/1.1 404 Not Found\n\n404 Not Found'
        except timeout:
            print("timed out")
            reply = 'HTTP/1.1 408 Request Timed Out\n\n408 Request Timed Out'
        except BadRequest:
            reply = 'HTTP/1.1 400 Bad Request\n\n400 Bad Request'


        # Send the reply
        # try:
        connectionSocket.sendall(reply.encode())
        # print("reply sent: ", reply)

        # except timeout:
        #     reply = 'HTTP/1.1 408 Request Timed Out\n\n408 Request Timed Out'

        # Close connection to client (but not welcoming socket)
        connectionSocket.close()

    serverSocket.close()

if __name__=='__main__':
    main()