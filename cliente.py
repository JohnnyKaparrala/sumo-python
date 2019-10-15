import pygame
import time
import socket
from enums import *
from threading import Thread
from Rikishi import Rikishi
from Position import Position2D

pygame.init()
screen = pygame.display.set_mode((400, 300))
done = False


clock = pygame.time.Clock()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(0.1)  

actCon = ActCon()
coms = Coms()

acoes = [False] * (actCon.QTD_ACOES)

ADDR_SERV = "177.220.18.65"#177.220.18.66
PORT_SERV = 12000
ADDR = (ADDR_SERV, PORT_SERV)

rikishis = {}

#pygame.display.iconify()

def mandar_pro_serv (conteudo):
    #print(conteudo.decode())
    client_socket.sendto(conteudo, ADDR)

mandar_pro_serv(("com:" + str(coms.ENTRAR)).encode())

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
            elif tipo == "rpos":
                print(comando)
                rikishis[comando.split("/")[0]].Centre = (int(comando.split("/")[1]) , int(comando.split("/")[2]))
            elif tipo == "gobj":
                aux = Rikishi(r = 60, pos=Position2D(0,0), color = (155,0,0))
                aux.fromStr(comando.split("/")[0])
                rikishis[comando.split("/")[0]] = aux
                print("rikishi inserido")
                #rikishis[ip] = novo rikishi
                pass
            
        except socket.timeout:
            continue

ouvir = Thread(target = ouvir_do_serv, args = ())
ouvir.start()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            
    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_UP]: mandar_pro_serv(("act:" + str(actCon.UP)).encode())
    if pressed[pygame.K_DOWN]: mandar_pro_serv(("act:" + str(actCon.DOWN)).encode())
    if pressed[pygame.K_LEFT]: mandar_pro_serv(("act:" + str(actCon.LEFT)).encode())
    if pressed[pygame.K_RIGHT]: mandar_pro_serv(("act:" + str(actCon.RIGHT)).encode())

    for bola in list(rikishis):
        screen.fill((0, 0, 0))
        bola.render(screen)
        pygame.display.flip()
    clock.tick(60)
