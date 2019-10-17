import socket
import pygame
from Rikishi import Rikishi
from Position import Position2D
from enums import *
from Directions import Directions
from threading import Thread

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
enderecos_ip = []
try:
    server_socket.bind(('', 12000))
except OSError:
    print("porta em uso")
    exit()

print("esperando o cliente..")
recebendo = False

server_socket.settimeout(1)
rikishis = {}
rikishi_pode_receber = {}
comandos_guardados_dos_rikishis = {}
clock = pygame.time.Clock()

def broadcast (conteudo):
    #print("b")
    for add in enderecos_ip:#manda as novas prop dos objetos
        #print(add)
        
        try:
            #if rikishi_pode_receber[str(add)]:
            print(conteudo.decode())
            server_socket.sendto(conteudo, add)
        except:
            #enderecos_ip.remove(add)
            pass

def game_loop ():
    while True:
        for add in rikishis:
            #print(comandos_guardados_dos_rikishis[add])
            if comandos_guardados_dos_rikishis[add][ActCon.UP]:
                rikishis[add].accelToward(Directions.UP)
            elif comandos_guardados_dos_rikishis[add][ActCon.DOWN]:
                rikishis[add].accelToward(Directions.DOWN)
            else:
                rikishis[add].stopAccelToward(Directions.DOWN)
            
            if comandos_guardados_dos_rikishis[add][ActCon.LEFT]:
                rikishis[add].accelToward(Directions.LEFT)
            elif comandos_guardados_dos_rikishis[add][ActCon.RIGHT]:
                rikishis[add].accelToward(Directions.RIGHT)
            else:
                rikishis[add].stopAccelToward(Directions.RIGHT)

            comandos_guardados_dos_rikishis[add][ActCon.UP] = False
            comandos_guardados_dos_rikishis[add][ActCon.DOWN] = False
            comandos_guardados_dos_rikishis[add][ActCon.LEFT] = False
            comandos_guardados_dos_rikishis[add][ActCon.RIGHT] = False

            rikishis[add].process()

            broadcast(("rpos:" + str(add) + "/" + str(rikishis[add].Centre.X) + "/" + str(rikishis[add].Centre.Y)).encode())

        clock.tick(60)

t_loop = Thread(target = game_loop, args = ())
t_loop.start()
while True:
    try:
        message, address = server_socket.recvfrom(1024)
        mes = message.decode()
        tipo = mes.split(":")[0]
        comando = mes.split(":")[1]
        
        print ("msg de " + str(address) + "; msg: " + mes)
        if (address not in enderecos_ip):
            enderecos_ip.append(address)
            #print(str(enderecos_ip))
            print ("endereco " + str(address) + " adicionado")

        if tipo == "com":
            if int(comando) == Coms.ENTRAR:
                rikishis[str(address)] = Rikishi(r = 60, pos=Position2D(0,0), color = (155,0,0))
                rikishi_pode_receber[str(address)] = False
                comandos_guardados_dos_rikishis[str(address)] = [False] * ActCon.QTD_ACOES
                print(str(rikishis[str(address)]))
                broadcast(("gobj:" + str(address) + "/" + str(rikishis[str(address)])).encode())
        elif tipo == "act":
            print("acao: " + comando)
            #atualiza os objetos do game baseado na acao
            comandos_guardados_dos_rikishis[str(address)][int(comando)] = True
            print(comandos_guardados_dos_rikishis[str(address)][int(comando)])
            print(comandos_guardados_dos_rikishis[str(address)])
        elif tipo == "rec":
            rikishi_pode_receber[str(address)] = True

    except socket.timeout:
        if(recebendo):
            print ("um pacote foi perdido")