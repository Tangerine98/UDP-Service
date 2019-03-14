import socket

ip_addr = '127.0.0.1'
udp_port = 6789
max_bytes = 10000

if __name__ == '__main__' :
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    msg = bytes("Hello",'utf-8')
    client.sendto(msg, (ip_addr, udp_port))

    data, addr = client.recvfrom(max_bytes)
    message = str(data.decode())
    print("Message: ",message)