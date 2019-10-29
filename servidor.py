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

dentro_da_sala = 0
enderecos = []

centro = Position2D(x=400,y=300)
raio = 300

def broadcast (conteudo):
    #print("b")
    for add in enderecos_ip:#manda as novas prop dos objetos
        #print(add)
        
        try:
            #if rikishi_pode_receber[str(add)]:
            #print(conteudo.decode())
            server_socket.sendto(conteudo, add)
        except:
            #enderecos_ip.remove(add)
            pass

def mandar_para_cliente (conteudo, add):
    try:
        server_socket.sendto(conteudo, add)
    except socket.timeout:
        mandar_para_cliente(conteudo, add)
        pass

def game_loop ():
    while True:
        for add in list(rikishis):
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

            
            if dentro_da_sala == 2:
                print("tem2")
                riki1 = rikishis[enderecos[0]]
                riki2 = rikishis[enderecos[1]]

                if(riki1.hasCollision(riki2)):
                    riki1.transferMomentum(riki2)
                    riki2.transferMomentum(riki1)

                if(centro.distance(riki1.Centre)> raio):
                    print("2 ganhou")
                    exit()

                if(centro.distance(riki2.Centre)> raio):
                    print("1 ganhou")
                    exit()
            
            rikishis[add].process()
            
            broadcast(("rpos:" + str(add) + "/" + str(rikishis[add].Centre.X) + "/" + str(rikishis[add].Centre.Y)).encode())

        clock.tick(30)

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
                recebendo = True
                enderecos.append(str(address))
                dentro_da_sala += 1

                rikishis[str(address)] = Rikishi(r = 20, pos= Position2D(400,140) if dentro_da_sala == 1 else Position2D(400,460), color = (155,0,0))
                rikishi_pode_receber[str(address)] = False
                comandos_guardados_dos_rikishis[str(address)] = [False] * ActCon.QTD_ACOES
                print(str(rikishis[str(address)]))
                broadcast(("gobj:" + str(address) + "/" + str(rikishis[str(address)])).encode())
                for add_cliente in rikishis:
                    if (add_cliente != str(address)):
                        mandar_para_cliente(("gobj:" + str(add_cliente) + "/" + str(rikishis[str(add_cliente)])).encode(),address)
            elif int(comando) == Coms.SAIR:
                enderecos_ip.remove(address)
                    
                del rikishis[str(address)]
                del rikishi_pode_receber[str(address)]
                del comandos_guardados_dos_rikishis[str(address)]
                dentro_da_sala -=1
                broadcast(("saiu:" + str(address)).encode())
        elif tipo == "act":
            #print("acao: " + comando)
            #atualiza os objetos do game baseado na acao
            comandos_guardados_dos_rikishis[str(address)][int(comando)] = True
            #print(comandos_guardados_dos_rikishis[str(address)][int(comando)])
            #print(comandos_guardados_dos_rikishis[str(address)])
        elif tipo == "rec":
            rikishi_pode_receber[str(address)] = True

    except socket.timeout:
        if(recebendo):
            print ("um pacote foi perdido")