import pygame
import time
import socket
from enums import *
from threading import Thread

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False


clock = pygame.time.Clock()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(0.1)  

acoes = [False] * ActCon.QTD_ACOES

ADDR_SERV = "177.220.18.65"#177.220.18.66
PORT_SERV = 12000
ADDR = (ADDR_SERV, PORT_SERV)

pygame.display.iconify()
mandar_pro_serv(("com:" + str(Coms.ENTRAR)).encode())

rikishis = {}

def ouvir_do_serv():
    while not done:
        try:
            data, server = client_socket.recvfrom(1024)
            mes = data.decode()
            tipo = mes.split(":")[0]
            comando = mes.split(":")[1]

            if tipo == "act":
                #atualiza os objetos do game baseado na acao
                if comando.isdigit():
                    acoes[int(comando)] = True
            elif tipo == "gobj":
                #rikishis[ip] = novo rikishi
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
    
    if pressed[pygame.K_UP]: mandar_pro_serv(("act:" + str(ActCon.UP)).encode())
    if pressed[pygame.K_DOWN]: mandar_pro_serv(("act:" + str(ActCon.DOWN)).encode())
    if pressed[pygame.K_LEFT]: mandar_pro_serv(("act:" + str(ActCon.LEFT)).encode())
    if pressed[pygame.K_RIGHT]: mandar_pro_serv(("act:" + str(ActCon.RIGHT)).encode())
    
    screen.fill((0, 0, 0))
    color = (255, 100, 0)
    pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
    
    pygame.display.flip()
    clock.tick(60)
