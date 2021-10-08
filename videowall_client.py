import socket
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
MESSAGE = open('/usr/share/rpd-wallpaper/raspberry-pi-logo.png', 'rb').read()
MULTICAST_TTL = 2

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
    while True:
        print('Sending...')
        sock.sendto(MESSAGE, (MCAST_GRP, MCAST_PORT))