import socket
import os
import sys
import base64
import shutil

ip_addr = '127.0.0.1'
udp_port = 8000
max_bytes = 10240

repo_path = os.path.dirname(os.path.abspath(__file__)) + '/'

def subtract(path):
    return "".join(path.rsplit(repo_path))

if __name__ == '__main__' :
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((ip_addr, udp_port))
    print('Server started at ',ip_addr,':',udp_port)
    os.chdir(repo_path + 'file-server/')
    while True:

        op, addr = server.recvfrom(max_bytes)
        op = int(str(op.decode()))

        if op == 1:
            path = os.path.split(os.getcwd())[1]
            server.sendto(bytes(path,'utf-8'), addr)

        elif op == 2:
            path = os.path.dirname(os.path.abspath(__file__)) + '/'

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

        elif op == 3:
            path = os.path.dirname(os.path.abspath(__file__)) + '/'

            data, addr = server.recvfrom(max_bytes)
            folder_name = path + str(data.decode())

            try:
                os.mkdir(folder_name)
            except OSError:
                message = "Creation of directory {} failed..".format(folder_name)
            else:
                message = "Successfully created directory {}..".format(subtract(path) + str(data.decode()))
            server.sendto(bytes(message,'utf-8'), addr)

        elif op == 4:
            path = os.path.dirname(os.path.abspath(__file__)) + '/'

            data, addr = server.recvfrom(max_bytes)
            if str(data.decode()) == '..':
                folder_name = str(data.decode())
            else:
                folder_name = path + str(data.decode())

            try:
                os.chdir(folder_name)
            except OSError:
                return_string = "Cannot move into directory {}.. Have you entered complete path??".format(folder_name)
            else:
                if folder_name == '..' :
                    return_string = "Successfully moved into parent directory"
                else:
                    return_string = "Successfully moved into folder {}".format(subtract(path) + str(data.decode()))
            server.sendto(bytes(return_string,'utf-8'), addr)

        elif op == 5:
            path = os.path.dirname(os.path.abspath(__file__)) + '/'

            data, addr = server.recvfrom(max_bytes)
            folder_name = path + str(data.decode())
            print("Directory to be deleted: ", (subtract(path) + str(data.decode())))

            try:
                shutil.rmtree(folder_name)
            except OSError:
                return_string = "Deletion of the directory %s failed" % (subtract(path) + str(data.decode()))
            else:
                return_string = "Successfully deleted the directory %s" % (subtract(path) + str(data.decode()))
            server.sendto(bytes(return_string,'utf-8'), addr)

        elif op == 6:
            path = os.path.dirname(os.path.abspath(__file__)) + '/'

            file_name, addr = server.recvfrom(max_bytes)
            file_name = str(file_name.decode())
            data, addr = server.recvfrom(max_bytes)
            try:
                file_content = base64.b64decode(data)
                file = open(file_name, 'wb')
                file.write(file_content)
                return_string = "File {} uploaded to folder {}".format(file_name, subtract(path))
            except:
                return_string = "File upload failed"
            server.sendto(bytes(return_string,'utf-8'), addr)

        elif op == 7:
            path = os.path.dirname(os.path.abspath(__file__)) + '/'

            data, addr = server.recvfrom(max_bytes)
            file_name = str(data.decode())
            print("\nRequested File : ",file_name)
            file_name = path + str(data.decode())

            exists = os.path.isfile(file_name)
            if exists:
                file = open(file_name, 'rb')
                file_content = file.read()
                base64_format = base64.encodestring(file_content)
                server.sendto(base64_format, addr)
            else:
                message = bytes("File doesn't exist",'utf-8')
                server.sendto(message, addr)

        elif op == 8:
            path = os.path.dirname(os.path.abspath(__file__)) + '/'

            data, addr = server.recvfrom(max_bytes)
            file_name = path + str(data.decode())
            print("\nFile to be deleted : ", subtract(path) + str(data.decode()))

            try:
                os.remove(file_name)
            except OSError:
                return_string = "Deletion of file {} failed".format(subtract(path) + str(data.decode()))
            else:
                return_string = "Successfully deleted file {}".format(subtract(path) + str(data.decode()))
            server.sendto(bytes(return_string,'utf-8'), addr)

        elif op == 9:
            print('\nConnection terminated')
            sys.exit()