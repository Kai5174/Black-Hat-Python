# -*- coding: utf-8 -*-
import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print("[!!] Failed to listen on {}:{}".format(local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions")
        sys.exit(0)
    
    print("[*] Listening on {}:{}".format(local_host, local_port))

    server.listen(100)

    while 1:
        client_socket, addr = server.accept()
        print("[==>] Received incoming connection from {}:{}".format(addr[0], addr[1]))
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    print("[*] Trying to connect {}:{}".format(remote_host, remote_port))
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    print("[*] Connected to {}:{}".format(remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):
            print("[<==] Sending {} bytes to localhost.".format(len(remote_buffer)))
            client_socket.send(remote_buffer)
    
    while 1:
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[==>] Received {} bytes from localhost.".format(len(local_buffer)))
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)

            remote_socket.send(local_buffer)
            print("[==>] sent to remote.")

        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print("[<==] Received {} bytes from remote.".format(len(remote_buffer)))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)

            client_socket.send(remote_buffer)

            print("[<==] Sent to localhost.")
        
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()

            print("[*] No more data. Closing connections")

            break


def receive_from(connection):

    recv_buffer = b""

    connection.settimeout(10)

    try:
        while 1:
            data = connection.recv(4096)
            if len(data) < 4096:
                recv_buffer += data
                break
            recv_buffer += data
    except Exception as e:
        print("Exception in receive_from: {}".format(e))
    
    return recv_buffer


def response_handler(remote_buffer):
    # TODO: 你想改包就在这儿改
    return remote_buffer

def request_handler(local_buffer):
    # TODO: 你想改包就在这儿改
    return local_buffer

def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join([b"%0*X" % (digits, x)  for x in s])
        text = ''.join([chr(x) if 0x20 <= x < 0x7F else '.'  for x in s]).encode()
        result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )

    
    print(b''.join(result).decode())


def main():

    if len(sys.argv[1:]) != 5:
        print("Usage: python proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: python proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
    
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

main()
