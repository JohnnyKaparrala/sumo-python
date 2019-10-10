import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
enderecos_ip = []
try:
    server_socket.bind(('', 12000))
except OSError:
    print("porta em uso")
    exit()

print("esperando o cliente..")
recebendo = False
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

server_socket.settimeout(0.1)
circulos_jogadores = {}
while True:
    try:
        message, address = server_socket.recvfrom(1024)
        mes = message.decode()
        
        print ("msg de " + str(address) + "; msg: " + mes)
        if (address not in enderecos_ip):
            enderecos_ip.append(address)
            #print(str(enderecos_ip))
            circulos_jogadores[str(address)] = (x,y)
            print ("endereco " + str(address) + " adicionado")
        
        if mes.split(":")[0] == "act":
            #atualiza os objetos do game baseado na acao
            print(enderecos_ip)
            for add in enderecos_ip:#manda as novas prop dos objetos
                print ("mandando " + mes)
                try:
                    server_socket.sendto(mes.encode(), add)
                except:
                    enderecos_ip.remove(add)

    except socket.timeout:
        if(recebendo):
            print ("um pacote foi perdido")