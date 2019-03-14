import socket
import os
#import base64

ip_addr = '127.0.0.1'
udp_port = 8000
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
            file_size = os.path.getsize(msg)
            if file_size < 10000000 :
                if file_size > 1000000 :
                    return_string = "File exists and it's size is {} MB".format(file_size/1000000)
                else :
                    return_string = "File exists and it's size is {} bytes".format(file_size)
            else :
                return_string = "File can't be transferred since it has size greater than 10MB"
            message = bytes(return_string,'utf-8')
            server.sendto(message, addr)
        else:
            message = bytes("File doesn't exist",'utf-8')
            server.sendto(message, addr)
        
        #with open("yourfile.ext", "rb") as image_file:
            #encoded_string = base64.b64encode(image_file.read())

            #print('File : ',encoded_string)