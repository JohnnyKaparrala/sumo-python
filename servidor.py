import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
enderecos = []
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
while True:
    try:
        message, address = server_socket.recvfrom(1024)
        mes = message.decode()
        
        print("msg de " + str(address) + "; msg: " + mes)
        server_socket.sendto(mes.encode(), address)
    except socket.timeout:
        if(recebendo):
            print("um pacote foi perdido")