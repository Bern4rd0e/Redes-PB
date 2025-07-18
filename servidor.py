import socket
# import psutil

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0, 5551"))
s.listen(5)

while True:
    clientesocket, address = s.accept()
    print(f"Conexão do endereço {address} foi ESTABELECIDA")

    msg = clientesocket.recv(12)
    comando = msg.decode("utf-8")

    if comando == "/help":
        clientesocket.send(bytes(f"Ajuda Requisitada: \n \t "
                                 "Comandos: \n \t "
                                 "/men -> para ver a memória \n \t"
                                 "/off -> para desligar"
                                 ""
                                 
                                 ))