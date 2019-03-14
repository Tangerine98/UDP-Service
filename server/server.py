import socket
import os
import base64

ip_addr = '127.0.0.1'
udp_port = 8000
max_bytes = 10000000

if __name__ == '__main__' :
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((ip_addr, udp_port))
    print('Server started at ',ip_addr,':',udp_port)
    while True:
        data, addr = server.recvfrom(max_bytes)
        file_name = str(data.decode())
            
        exists = os.path.isfile(file_name)
        if exists:
            file_size = os.path.getsize(file_name)
            if file_size < 10000000 :
                file = open(file_name, 'rb')
                file_content = file.read()
                base64_format = base64.encodestring(file_content)
                server.sendto(base64_format, addr)
            else :
                return_string = "File can't be transferred since it has size greater than 10MB"
                message = bytes(return_string,'utf-8')
                server.sendto(message, addr)
        else:
            message = bytes("File doesn't exist",'utf-8')
            server.sendto(message, addr)