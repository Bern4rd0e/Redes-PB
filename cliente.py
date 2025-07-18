import socket

# TCP/IP 
# socket.AF_INET -> protocolo IPv4      

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 5551))

cmd = input("Insira o Comando: ")

s.send(cmd.encode("utf-8"))

msg = s.recv(1024)

print(f"Mensagem: {msg.decode("utf-8")}")