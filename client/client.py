import socket
import sys
import base64

ip_addr = '127.0.0.1'
udp_port = 8000
max_bytes = 10240

def menu() :
    print("MENU:-")
    print("\t1. List all files")
    print("\t2. Get a file")
    print("\t3. Exit")
    op = int(input("Enter your choice: "))
    return op

if __name__ == '__main__' :
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        op = menu()
        client.sendto(bytes(str(op),'utf-8'), (ip_addr,udp_port))

        if op == 1:
            data,addr = client.recvfrom(max_bytes)
            print(str(data.decode()))

        elif op == 2:
            msg = input("\nEnter file name: ")
            client.sendto(bytes(msg,'utf-8'), (ip_addr, udp_port))

            data, addr = client.recvfrom(max_bytes)
            try:
                file_content = base64.b64decode(data)

                file = open(msg, 'wb')
                file.write(file_content)
                print("File {} downloaded".format(msg))
            except:
                message = str(data.decode())
                print(message)

        elif op == 3:
            client.sendto(bytes("Stop",'utf-8'), (ip_addr,udp_port))
            print('\nTerminating connection..')
            sys.exit()

        else:
            print('\nInvalid option\n')


        