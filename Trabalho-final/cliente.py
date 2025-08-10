import socket
import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from coletor import ColetorDadosSistema, chave
import binascii  # para mostrar bytes em hexadecimal

class Cliente:
    BROADCAST_PORT = 50000
    BROADCAST_MESSAGE = b'SOLICITACAO_DESCOBERTA'
    RESPONSE_MESSAGE = b'RESPOSTA_DESCOBERTA'

    def __init__(self):
        pass

    def escutar_broadcast(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp.bind(('', self.BROADCAST_PORT))

        print("Cliente aguardando broadcast do servidor...")
        while True:
            data, addr = udp.recvfrom(1024)
            if data == self.BROADCAST_MESSAGE:
                ip_servidor = addr[0]
                print(f"Broadcast recebido de {ip_servidor}")
                udp.sendto(self.RESPONSE_MESSAGE, addr)
                udp.close()
                return ip_servidor

    def enviar_dados(self, ip_servidor):
        coletor = ColetorDadosSistema()
        dados = coletor.coletar_todos_os_dados()
        dados_json = json.dumps(dados).encode('utf-8')

        # Mostrar dados antes da criptografia
        print("Dados JSON (texto claro):")
        print(dados_json.decode('utf-8'))

        nonce = get_random_bytes(16)
        cipher = AES.new(chave, AES.MODE_EAX, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(dados_json)

        # Mostrar dados criptografados em hexadecimal
        print("Nonce (hex):", binascii.hexlify(nonce).decode())
        print("Tag (hex):", binascii.hexlify(tag).decode())
        print("Ciphertext (hex):", binascii.hexlify(ciphertext).decode())

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.connect((ip_servidor, self.BROADCAST_PORT))

        print(f"Conectado a {ip_servidor} via TCP, enviando dados criptografados...")
        tcp.sendall(nonce + tag + ciphertext)
        tcp.close()
        print("Dados enviados com sucesso!")

    def main(self):
        ip_servidor = self.escutar_broadcast()
        self.enviar_dados(ip_servidor)

if __name__ == "__main__":
    cliente = Cliente()
    cliente.main()
