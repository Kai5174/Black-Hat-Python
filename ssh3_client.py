import threading
import paramiko
import subprocess
import sys
import getpass


def ssh_connector(ip, port=22):
    user = input('username: ')
    passwd = getpass.getpass(prompt="password: ", stream=None)

    host = ip + ":" + str(port)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("[*] connecting to {}".format(host))
    client.connect(hostname=ip, port=port, username=user, password=passwd)
    print("[+] connected to {}".format(host))
    while 1:
        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
            command = input('connected > ')
            if command == 'exit':
                sys.exit(0)
            ssh_session.exec_command(command)
            print(ssh_session.recv(1024).decode())

def main():
    if len(sys.argv[1:]) != 2:
        print("Usage: python ssh3_client.py [remoteip] [remoteport]")
        print("Example: python ssh3_client.py 192.168.17.133 22")
        sys.exit(0)
    
    ip = sys.argv[1]
    port = int(sys.argv[2])
    ssh_connector(ip, port)

if __name__ == '__main__':
    main()
