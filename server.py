import socket
import os
#import base64

ip_addr = '127.0.0.1'
udp_port = 6789
max_bytes = 10000

if __name__ == '__main__' :
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((ip_addr, udp_port))
    print('Server started at ',ip_addr,':',udp_port)
    while True:
        data, addr = server.recvfrom(max_bytes)
        msg = str(data.decode())
        print("File Name: ", msg)
            
        exists = os.path.isfile(msg)
        if exists:
            message = bytes("File exists",'utf-8')
            server.sendto(message, addr)
        else:
            message = bytes("File doesn't exist",'utf-8')
            server.sendto(message, addr)
        
        #with open("yourfile.ext", "rb") as image_file:
            #encoded_string = base64.b64encode(image_file.read())

            #print('File : ',encoded_string)