import socket 

# TCP/IP 
# socket.AF_INET -> protocolo IPv4      

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 5551))

class Cliente:
    def __init__(self, op):
        self.set_op(op)

    def set_op(self, op):
        self.__op = op

    def get_op(self):
        return self.__op

    def __str__(self):
        return f"Opcoes: {self.__op}"

    def to_dict(self):
        return{
            "Opcoes": self.__op
        }

class Clientes:
    def main():
        cmd = input("Insira o Comando: ")

        s.send(cmd.encode("utf-8")) # conversão de texto para bytes

        msg = s.recv(1024)

        print(f"Mensagem: {msg.decode("utf-8")}")
