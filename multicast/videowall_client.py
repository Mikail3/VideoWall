# Multicast receiver
# Guidance:  https://stackoverflow.com/a/1794373
import socket
import struct
import io
import pygame

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill((0, 0, 0))
pygame.display.update()

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    running = True
    while running:
        data = io.BytesIO(sock.recv(102400))
        screen.blit(pygame.image.load(data), (0, 0))
        pygame.display.update()
        print('Boop...')
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                running = False