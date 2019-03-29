import socket
import os
import sys
import base64

ip_addr = '127.0.0.1'
udp_port = 8000
max_bytes = 10240

if __name__ == '__main__' :
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((ip_addr, udp_port))
    print('Server started at ',ip_addr,':',udp_port)
    #print('Waiting for connection..')
    while True:

        op, addr = server.recvfrom(max_bytes)
        #print("\nConnected to client at port: {}".format(addr[1]))
        op = int(str(op.decode()))

        if op == 1:
            path = 'images/'

            files = os.listdir(path)
            file_list = "\nFILE LIST:-\n"
            folder_list = "\nDIRECTORY LIST:-\n"
            for name in files:
                file_exists = os.path.isfile(path+name)
                folder_exists = os.path.isdir(path+name)
                if file_exists:
                    file_list = file_list + name + "\n"
                elif folder_exists:
                    folder_list = folder_list + name + "\n"
            file_list = folder_list + file_list
            print('Sending list of files..')
            server.sendto(bytes(file_list,'utf-8'), addr)

        elif op == 2:
            data, addr = server.recvfrom(max_bytes)
            folder_name = str(data.decode())

            try:
                os.mkdir(folder_name)
            except OSError:
                message = "Creation of directory {} failed..".format(folder_name)
            else:
                message = "Successfully created directory {}..".format(folder_name)
            server.sendto(bytes(message,'utf-8'), addr)

        elif op == 3:
            data, addr = server.recvfrom(max_bytes)
            folder_name = str(data.decode())

            try:
                os.chdir(folder_name)
            except OSError:
                return_string = "Cannot move into directory {}.. Have you entered complete path??".format(folder_name)
            else:
                return_string = "Successfully moved into folder {}".format(folder_name)
            server.sendto(bytes(return_string,'utf-8'), addr)

        elif op == 6:
            data, addr = server.recvfrom(max_bytes)
            file_name = str(data.decode())
            print("\nRequested File : ",file_name)
            file_name = 'images/'+str(data.decode())

            exists = os.path.isfile(file_name)
            if exists:
                file_size = os.path.getsize(file_name)
                if file_size < max_bytes :
                    file = open(file_name, 'rb')
                    file_content = file.read()
                    base64_format = base64.encodestring(file_content)
                    server.sendto(base64_format, addr)
                else :
                    return_string = "File can't be transferred since it has size greater than 10KB"
                    message = bytes(return_string,'utf-8')
                    server.sendto(message, addr)
            else:
                message = bytes("File doesn't exist",'utf-8')
                server.sendto(message, addr)

        elif op == 7:
            data, addr = server.recvfrom(max_bytes)
            file_name = str(data.decode())
            print("\nFile to be deleted : ", file_name)

            try:
                os.remove(file_name)
            except OSError:
                return_string = "Deletion of file {} failed".format(file_name)
            else:
                return_string = "Successsfully deleted file {}".format(file_name)
            server.sendto(bytes(return_string,'utf-8'), addr)

        elif op == 8:
            print('\nConnection terminated')
            sys.exit()