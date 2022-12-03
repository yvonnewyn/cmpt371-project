# Include Python's Socket Library
from socket import *
import struct

# reference: https://docs.python.org/3/howto/sockets.html
# class my_socket:
#     def __init__(self, sock=None):
#         if sock is None:
#             self.sock = socket(AF_INET,SOCK_STREAM)
#         else:
#             self.sock = sock

#     def bind(self, host, port):
#         self.sock.bind((host, port))

class my_packet:
    def __init__(self, family=AF_INET, type=SOCKET_STREAM, src_port, dest_port=80, src, dest='localhost', data=''):
        self.src_port = src_port
        self.dest_port = dest_port
        self.src = src
        self.dest = dest
        self.data = data
        self.pkt = None
        self.create()

    def create(self):
        self.src = self.src_port
        self.dest = self.dest_port
        self.seq_num = 0
        self.ack_num = 0
        self.offset = 5 # number of 32-bit words
        self.flags = 0 # ????
        self.win_size = htons(5840)
        self.checksum = 0
        self.urg_ptr = 0

        return

    def pack(self):
        self.pkt = struct.pack('!HHLLBBHHH',
                    self.src,
                    self.dest,
                    self.seq_num,
                    self.ack_num,
                    self.offset,
                    self.flags,
                    self.win_size,
                    self.checksum,
                    self.urg_ptr)
        self.get_checksum()
        return

    # def get_checksum(self):

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
serverSocket.listen(1) # change 1 to bigger number so connections are able to be queued up
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

            # reply = 'HTTP/1.0 200 OK\n\n' + content

            reply = struct.pack()

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


