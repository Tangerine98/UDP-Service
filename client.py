import socket
import base64

ip_addr = '127.0.0.1'
udp_port = 8000
max_bytes = 10000

if __name__ == '__main__' :
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    msg = input("Enter file name: ")
    client.sendto(bytes(msg,'utf-8'), (ip_addr, udp_port))

    data, addr = client.recvfrom(max_bytes)
    message = base64.b64decode(data)
    #message = data.decode('ascii')
    print("Message: ",message)