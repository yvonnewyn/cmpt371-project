# Include Python's Socket Library
from socket import *
import struct
import pathlib
from datetime import datetime
import threading
import time


# threading.Thread(target, args)

threads = []

class BadRequest(Exception):
    pass

def newTCPServerThread(connectionSocket, start):

        print(len(threads))

        request = connectionSocket.recv(1024)
        print(request)

        if not request:
            print('timeout')
            reply = 'HTTP/1.1 408 Request Timed Out\r\nConnection: close\n\n408 Request Timed Out'
        request = request.decode()
        end = time.time()

        if (end-start)>60:
            reply = 'HTTP/1.1 408 Request Timed Out\r\nConnection: close\n\n408 Request Timed Out'
            connectionSocket.sendall(reply.encode())
            # Close connection to client (but not welcoming socket)
            connectionSocket.close() 
            return

        else:
            filename, c_get, date = request_info(request)

            if (filename == '/'):
                filename = 'test.html'
            else:
                filename = filename[1:]

            if c_get:
                mdate = pathlib.Path('server/' + filename).stat().st_mtime
                # mdate = datetime.fromtimestamp(mdate, tz=timezone.utc)
                mdate = datetime.fromtimestamp(mdate).strftime('%a, %-d %b %Y %H:%M:%S')
                date_time = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S')
                mdate_time = datetime.strptime(mdate, '%a, %d %b %Y %H:%M:%S')
                # print(date, mdate)
                if mdate_time <= date_time:
                    reply = 'HTTP/1.1 304 Not Modified\n\n'
                else:
                    f = open('server/' + filename)
                    content = f.read()
                    f.close()
                    reply = 'HTTP/1.1 200 OK\n\n' + content
    
            else:
                try:
                    f = open('server/' + filename)
                    content = f.read()
                    f.close()

                    reply = 'HTTP/1.1 200 OK\n\n' + content

                except FileNotFoundError:
                    reply = 'HTTP/1.1 404 Not Found\n\n404 Not Found'

        # Send the reply
        try:
            connectionSocket.sendall(reply.encode())

        except timeout:
            reply = 'HTTP/1.1 408 Request Timed Out\n\n408 Request Timed Out'

        # Close connection to client (but not welcoming socket)
        connectionSocket.close()


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

    # Specify Server Port
    # serverHost = 'localhost'
    serverHost = ''
    serverPort = 8000

    # Create TCP welcoming socket
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # serverSocket.settimeout(30)

    # Bind the server port to the socket
    serverSocket.bind((serverHost,serverPort))

    # Server begins listerning foor incoming TCP connections
    serverSocket.listen(5)
    print ('Listening on port ', serverPort, '...')
    start = time.time()

    while True: # Loop forever
        # Server waits on accept for incoming requests.
        # New socket created on return
        try:
            connectionSocket, addr = serverSocket.accept()
            

            connectionSocket.settimeout(5)

            print(addr)

            newServerThread = threading.Thread(target=newTCPServerThread, args=[connectionSocket, start])
            # newServerThread = threading.Thread(target=newTCPServerThread, args=[serverSocket])
            threads.append(newServerThread)
            newServerThread.start()
            
        
        except timeout:
            print("timed out")
            reply = 'HTTP/1.1 408 Request Timed Out\r\nConnection: close\n\n408 Request Timed Out'
        except BadRequest:
            reply = 'HTTP/1.1 400 Bad Request\n\n400 Bad Request'
        except KeyboardInterrupt:
	        break
        start = time.time()

    for t in threads:
        t.join()

    serverSocket.close()

if __name__=='__main__':
    main()
