import socket
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

server_socket.settimeout(0.1)
rikishis = {}
comandos_guardados_dos_rikishis = {}

def broadcast (conteudo):
    #print("b")
    for add in enderecos_ip:#manda as novas prop dos objetos
        try:
            server_socket.sendto(conteudo, add)
        except:
            #enderecos_ip.remove(add)
            pass
            
def game_loop ():
    while True:
        for ip in list(rikishis):
            add = str(ip)
            #print(comandos_guardados_dos_rikishis[add])
            if comandos_guardados_dos_rikishis[add][ActCon.UP]:
                rikishis[add].accelToward(Directions.UP)
                comandos_guardados_dos_rikishis[add][ActCon.UP] = False
            else:
                rikishis[add].stopAccelToward(Directions.UP)
            if comandos_guardados_dos_rikishis[add][ActCon.LEFT]:
                rikishis[add].accelToward(Directions.LEFT)
                comandos_guardados_dos_rikishis[add][ActCon.LEFT] = False
            else:
                rikishis[add].stopAccelToward(Directions.LEFT)
            if comandos_guardados_dos_rikishis[add][ActCon.DOWN]:
                rikishis[add].accelToward(Directions.DOWN)
                comandos_guardados_dos_rikishis[add][ActCon.DOWN] = False
            else:
                rikishis[add].stopAccelToward(Directions.DOWN)
            if comandos_guardados_dos_rikishis[add][ActCon.RIGHT]:
                rikishis[add].accelToward(Directions.RIGHT)
                comandos_guardados_dos_rikishis[add][ActCon.RIGHT] = False
            else:
                rikishis[add].stopAccelToward(Directions.RIGHT)

            rikishis[add].process()
            broadcast(("rpos:" + str(add) + "/" + str(rikishis[add].Centre.X) + "/" + str(rikishis[add].Centre.Y)).encode())


lop = Thread(target = game_loop, args = ())
lop.start()
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
                comandos_guardados_dos_rikishis[str(address)] = [False] * ActCon.QTD_ACOES
                print(str(rikishis[str(address)]))
                broadcast(("gobj:" + str(address) + "/" + str(rikishis[str(address)])).encode())
        elif tipo == "act":
            print("acao: " + comando)
            #atualiza os objetos do game baseado na acao
            comandos_guardados_dos_rikishis[str(address)][int(comando)] = True
            print(comandos_guardados_dos_rikishis[str(address)][int(comando)])
            print(comandos_guardados_dos_rikishis[str(address)])


    except socket.timeout:
        if(recebendo):
            print ("um pacote foi perdido")