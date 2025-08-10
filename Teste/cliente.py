import socket
import psutil
import json

class Cliente:
    def __init__(self, server_ip, server_port=5551):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = None

    def listen_discover(self, listen_port=5552):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(('', listen_port))
        while True:
            data, addr = udp.recvfrom(1024)
            if data == b"DISCOVER_SERVER":
                udp.sendto(b"CLIENT_HERE", addr)


    def conectar(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.server_ip, self.server_port))

    def coletar_dados(self):
        dados = {
            'processadores': psutil.cpu_count(logical=True),
            'ram_livre': psutil.virtual_memory().available,
            'disco_livre': psutil.disk_usage('/').free,
            # você pode adicionar IPs, portas abertas, etc
        }
        return dados

    def enviar_dados(self):
        dados = self.coletar_dados()
        dados_json = json.dumps(dados).encode('utf-8')

        self.sock.sendall(dados_json)

        resposta = b""
        while True:
            parte = self.sock.recv(4096)
            if not parte:
                break
            resposta += parte
        return resposta.decode('utf-8')

    def fechar(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def main(self):
        try:
            self.conectar()
            resposta = self.enviar_dados()
            print("Resposta do servidor:", resposta)
        finally:
            self.fechar()

if __name__ == "__main__":
    cliente = Cliente("127.0.0.1", 5551)  # IP do servidor
    cliente.main()
