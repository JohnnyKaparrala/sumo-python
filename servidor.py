import socket
from Rikishi import Rikishi
from Position import Position2D
from enums import *
from Directions import Directions

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
    for add in enderecos_ip:#manda as novas prop dos objetos
        try:
            server_socket.sendto(conteudo, add)
        except:
            #enderecos_ip.remove(add)
            pass
def game_loop ():
    for ip in rikishis:
        if comandos_guardados_dos_rikishis[str(address)][ActCon.UP]:
            rikishis[ip].accelToward(Directions.UP)
            comandos_guardados_dos_rikishis[str(address)][ActCon.UP] = False
        else
            rikishis[ip].stopAccelToward(Directions.UP)
        if comandos_guardados_dos_rikishis[str(address)][ActCon.LEFT]:
            rikishis[ip].accelToward(Directions.LEFT)
            comandos_guardados_dos_rikishis[str(address)][ActCon.LEFT] = False
        else
            rikishis[ip].stopAccelToward(Directions.LEFT)
        if comandos_guardados_dos_rikishis[str(address)][ActCon.DOWN]:
            rikishis[ip].accelToward(Directions.DOWN)
            comandos_guardados_dos_rikishis[str(address)][ActCon.DOWN] = False
        else
            rikishis[ip].stopAccelToward(Directions.DOWN)
        if comandos_guardados_dos_rikishis[str(address)][ActCon.RIGHT]:
            rikishis[ip].accelToward(Directions.RIGHT)
            comandos_guardados_dos_rikishis[str(address)][ActCon.RIGHT] = False
        else
            rikishis[ip].stopAccelToward(Directions.RIGHT)

        rikishis[ip].process()

lop = Thread(target = game_loop, args = ())
while True:
    lop.start()

    try:
        message, address = server_socket.recvfrom(1024)
        mes = message.decode()
        tipo = mes.split(":")[0]
        comando = mes.split(":")[0]
        
        print ("msg de " + str(address) + "; msg: " + mes)
        if (address not in enderecos_ip):
            enderecos_ip.append(address)
            #print(str(enderecos_ip))
            print ("endereco " + str(address) + " adicionado")

        if tipo == "com":
            if comando == Coms.ENTRAR:
                rikishis[str(address)] = Rikishi(r = 60, pos=Position2D(0,0), color = (155,0,0))
                comandos_guardados_dos_rikishis[str(address)] = [False] * ActCon.QTD_ACOES
                broadcast(("gobj:" + str(rikishis)).encode())
        elif tipo == "act":
            #atualiza os objetos do game baseado na acao
            comandos_guardados_dos_rikishis[str(address)][int(comando)] = True
            print(enderecos_ip)
            broadcast(mes.encode())

    except socket.timeout:
        if(recebendo):
            print ("um pacote foi perdido")