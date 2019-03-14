import socket
import base64

ip_addr = '127.0.0.1'
udp_port = 8000
max_bytes = 10000000

if __name__ == '__main__' :
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    msg = input("Enter file name: ")
    client.sendto(bytes(msg,'utf-8'), (ip_addr, udp_port))

    data, addr = client.recvfrom(max_bytes)
    try:
        file_content = base64.b64decode(data)

        file = open(msg, 'wb')
        file.write(file_content)
    except:
        message = str(data.decode())
        print(message)