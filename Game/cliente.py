import pygame
import time
import socket
from enums import *
from threading import Thread
from Rikishi import Rikishi
from Position import Position2D

pygame.init()
screen = pygame.display.set_mode((800, 600))
centro = Position2D(x=400,y=300)
raio = 300
done = False

clock = pygame.time.Clock()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(0.01)  

actCon = ActCon()
coms = Coms()

ADDR_SERV = input("IP_Servidor: ")#"177.220.18.65"#177.220.18.66
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
            aux_com = comando

            if tipo == "rpos":
                x_pos = float(aux_com.split("/")[1])
                y_pos = float(aux_com.split("/")[2])
                rikishis[aux_com.split("/")[0]].Centre = Position2D(x_pos, y_pos)
                #print(aux_com.split("/")[1] + " " + aux_com.split("/")[2])
                #print ("nova pos:" + comando)
            elif tipo == "gobj":
                #print(comando)
                aux = Rikishi(r = 60, pos=Position2D(0,0), color = (155,0,0))
                aux.fromStr(comando.split("/")[1])
                #aux.convert_image()
                rikishis[comando.split("/")[0]] = aux
                #print("rikishi inserido")
                mandar_pro_serv("rec:1".encode())
                #rikishis[ip] = novo rikishi
            elif tipo == "saiu":
                del rikishis[str(comando)]

        except:
            continue

ouvir = Thread(target = ouvir_do_serv, args = ())
ouvir.start()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mandar_pro_serv(("com:" + str(coms.SAIR)).encode())
            done = True
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            
    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_UP]: mandar_pro_serv(("act:" + str(actCon.UP)).encode())
    if pressed[pygame.K_DOWN]: mandar_pro_serv(("act:" + str(actCon.DOWN)).encode())
    if pressed[pygame.K_LEFT]: mandar_pro_serv(("act:" + str(actCon.LEFT)).encode())
    if pressed[pygame.K_RIGHT]: mandar_pro_serv(("act:" + str(actCon.RIGHT)).encode())

    screen.fill((185,122,87))
    pygame.draw.circle(screen, (196,138,111), centro.toTuple(), centro.Y-1)
    pygame.draw.circle(screen, (99,62,41), centro.toTuple(), raio, 4)
    for bola in list(rikishis):
        rikishis[bola].render(screen)
    pygame.display.flip()
    clock.tick(30)
