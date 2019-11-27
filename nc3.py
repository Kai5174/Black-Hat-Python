# -*- coding: utf-8 -*-
# 中文

import sys
import socket
import getopt
import threading
import subprocess


listen = False
command = False
upload = False
execute = ''
target = ''
upload_destination = ''
filename = ''
port = 0

def usage():
    print("NetCat Tools for Python3")
    print("Usage: python nc3 -t target_host -p port")
    print("-l --listen                                                              - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run                                                 - execute the given file upon receiving a connection")
    print("-c --command                                                             - initialize a command shell")
    print("-u --upload=destination                                                  - upon receiving connection upload a file and write to [destination]")
    print("-f --filename=file_path_to_upload                                        - send the file to remote")
    print("\n")
    print("Examples: ")
    print("python nc3.py -t 192.168.0.1 -p 8989                                     :connect to 192.168.0.1:5555")
    print("python nc3.py -l -p 8989 -c                                              :start shell and waiting for connection")
    print("python nc3.py -t 192.168.0.1 -p 8989 -f /sth_to_upload                   :send the file to 192.168.0.1")
    print("python nc3.py -l -p 8989 -u /home/test.txt                               :save recv data to /home/test.txt")
    print("echo ABCDEDF |python nc3.py -t 192.168.0.1 -p 135                        :send ABCDEDF to 192.168.0.1")
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    global filename

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cuf:", ["help", "listen", "execute", "target", "port", "command", "upload", "filename"])
    except getopt.GetoptError as err:
        print("Error: {}".format(err))
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-f", "--filename"):
            filename = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandle Option"

    if not listen and len(target) and port > 0:
        if len(filename):
            with open(filename, 'rb') as f:
                data = f.read()
        else:
            data = sys.stdin.buffer.read()
        client_sender(data)

    if listen:
        server_loop()

def client_sender(buffer: bytes):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((target, port))
        if len(buffer) != 0:
            client.send(buffer)
        while True:
            recv_len = 1
            response = b""
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break
            try:
                print(response.decode(), end=' ')
            except:
                print(response.decode('gbk'), end=' ')
            buffer = input("").encode('utf-8')
            buffer += b"\n"
            client.send(buffer)
    except Exception as e:
        print("[*] Exception! Exiting. {}".format(e))

    client.close()

def server_loop():
    global target

    if not len(target):
        target = "0.0.0.0"
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    
    server.listen(5)

    while 1:
        client_socket, addr = server.accept()

        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command: bytes):
    command = command.rstrip().decode('utf-8')

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        output = "Failed to execute command. {} \n".format(e).encode()
    
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    if len(upload_destination):
        file_buffer = b""

        while 1:
            data = client_socket.recv(1024)

            if len(data) < 1024:
                file_buffer += data
                break
            else:
                file_buffer += data
        
        try:
            print(file_buffer)
            file_descriptor = open(upload_destination, 'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send("Successfully saved file to {}".format(upload_destination).encode('utf-8'))
        except Exception as e:
            client_socket.send("Failed to save file to {}, Exception {}".format(upload_destination, e).encode('utf-8'))
    
    if len(execute):
        output = run_command(execute)
        client_socket.send(output)
    
    if command:

        while 1:
            client_socket.send(b"<NC-PY3:#>")

            cmd_buffer = b""
            while b"\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            response = run_command(cmd_buffer)
            client_socket.send(response)
            
main()