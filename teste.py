import pygame
import time
import socket
from threading import Thread

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False
x = 30
y = 30

clock = pygame.time.Clock()

ADDR_SERV = "177.220.18.65"#177.220.18.66
PORT_SERV = 12000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(0.1)  

acoes = [False] * QTD_ACOES
circulos_jogadores = {}

mandar_pro_serv("com:ent")

def ouvir_do_serv():
    while not done:
        try:
            data, server = client_socket.recvfrom(1024)
            mes  = data.decode()
            if mes.split(":")[0] == "act":
                #atualiza os objetos do game baseado na acao
                if (mes.split(":")[1]).isdigit():
                    acoes[int((mes.split(":")[1]))] = True
            pass
        except socket.timeout:
            continue

def mandar_pro_serv (conteudo):
    #print(conteudo.decode())
    client_socket.sendto(conteudo, ADDR)

ouvir = Thread(target = ouvir_do_serv, args = ())
ouvir.start()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            
    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_UP]: mandar_pro_serv(("act:" + str(UP)).encode())
    if pressed[pygame.K_DOWN]: mandar_pro_serv(("act:" + str(DOWN)).encode())
    if pressed[pygame.K_LEFT]: mandar_pro_serv(("act:" + str(LEFT)).encode())
    if pressed[pygame.K_RIGHT]: mandar_pro_serv(("act:" + str(RIGHT)).encode())

    if acoes[UP]:
        y -= 3
        acoes[UP] = False
    if acoes[LEFT]:
        x -= 3
        acoes[LEFT] = False
    if acoes[DOWN]:
        y += 3
        acoes[DOWN] = False
    if acoes[RIGHT]:
        x += 3
        acoes[RIGHT] = False
    
    screen.fill((0, 0, 0))
    color = (255, 100, 0)
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
    
    pygame.display.flip()
    clock.tick(60)
