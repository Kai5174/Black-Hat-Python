import socket
import os
import struct
from ctypes import *
import threading
import time
from netaddr import IPNetwork, IPAddress

# -*- coding: utf-8 -*-

class ICMP(Structure):

    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("next_hop_mtu", c_ushort),
    ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer):
        pass


class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_ulong),
        ("dst", c_ulong),
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
        self.protocol_map = {
            1: 'ICMP',
            6: "TCP",
            17: "UDP"
        }

        self.src_addr = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_addr = socket.inet_ntoa(struct.pack("<L", self.dst))

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)




def scan(host, subnet, magic_message, t):

    if os.name == 'ht':
        # windows系统
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP
    
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))

    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    sniffer.settimeout(1)

    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    flag = 1
    
    try:
        while 1:
            if flag:
                t.start()
                flag = 0
            raw_buffer = sniffer.recvfrom(65565)[0]
            ip_hearder = IP(raw_buffer[0:20])
            # print("Protocol: %s %s -> %s" % (ip_hearder.protocol, ip_hearder.src_addr, ip_hearder.dst_addr))

            if ip_hearder.protocol == "ICMP":

                offset = ip_hearder.ihl * 4
                buf = raw_buffer[offset: offset + sizeof(ICMP)]

                icmp_header = ICMP(buf)

                # print("ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code))
                
                if icmp_header.code == 3 and icmp_header.type == 3:
                    if IPAddress(ip_hearder.src_addr) in IPNetwork(subnet):
                        if raw_buffer[len(raw_buffer)-len(magic_message):].decode() == magic_message:
                            print("Host Up: %s" % ip_hearder.src_addr)
                        
    except KeyboardInterrupt:
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    
    except socket.error:
        print("Done!")
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

def udp_sender(subnet, magic_message):
    sec = 0.5
    time.sleep(sec)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magic_message.encode(), ("%s" % ip, 65212))
            # print('sent')
        except:
            pass

            

def get_interface_ip(subnet):
    local_ip_list = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]
    for ip in local_ip_list:
        if ip in IPNetwork(subnet):
            return ip

def main():
    subnet = input("Tell me the subnet you want to scan: ")
    host = get_interface_ip(subnet)
    print("Your host is {}".format(host))
    # host = input("Tell me your IP: ")
    # host = '192.168.17.1'
    # subnet = '192.168.17.1/24'
    magic_message = "d7bdb5a397abf99b24a1a6bb7a1a"

    t = threading.Thread(target=udp_sender, args=(subnet, magic_message))

    scan(host, subnet, magic_message, t)

main()