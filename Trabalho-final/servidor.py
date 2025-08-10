import threading
import time
import socket
import json
import binascii
from Crypto.Cipher import AES
from coletor import chave

clientes_info = {}
stop_event = threading.Event()

class Servidor(threading.Thread):
    BROADCAST_PORT = 50000
    BROADCAST_MESSAGE = b'SOLICITACAO_DESCOBERTA'
    BROADCAST_INTERVAL = 3  # segundos entre broadcasts

    def __init__(self):
        super().__init__()
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind(('0.0.0.0', self.BROADCAST_PORT))
        self.tcp_socket.listen(5)

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def broadcast_loop(self):
        while not stop_event.is_set():
            print("[Broadcast] Enviando broadcast...")
            self.udp_socket.sendto(self.BROADCAST_MESSAGE, ('255.255.255.255', self.BROADCAST_PORT))
            time.sleep(self.BROADCAST_INTERVAL)

    def aceitar_conexoes(self):
        self.tcp_socket.settimeout(1)
        while not stop_event.is_set():
            try:
                conn, addr = self.tcp_socket.accept()
                print(f"[TCP] Conexão recebida de {addr}")

                pacote = conn.recv(65536)
                if len(pacote) < 32:
                    print("[TCP] Pacote inválido recebido, ignorando.")
                    conn.close()
                    continue

                nonce = pacote[:16]
                tag = pacote[16:32]
                ciphertext = pacote[32:]

                # Mostrar dados criptografados em hex
                print(f"[TCP] Dados recebidos (hex): nonce={binascii.hexlify(nonce).decode()}, tag={binascii.hexlify(tag).decode()}, ciphertext={binascii.hexlify(ciphertext).decode()}")

                cipher = AES.new(chave, AES.MODE_EAX, nonce=nonce)
                try:
                    dados_bytes = cipher.decrypt_and_verify(ciphertext, tag)
                    dados_cliente = json.loads(dados_bytes.decode('utf-8'))
                    clientes_info[addr[0]] = dados_cliente
                    print(f"[TCP] Dados descriptografados do cliente {addr[0]}:")
                    print(json.dumps(dados_cliente, indent=4))
                except Exception as e:
                    print(f"[TCP] Erro na descriptografia: {e}")

                conn.close()
            except socket.timeout:
                continue


    def run(self):
        broadcast_thread = threading.Thread(target=self.broadcast_loop)
        broadcast_thread.start()

        print("[Servidor] Aguardando conexões TCP...")
        try:
            self.aceitar_conexoes()
        finally:
            stop_event.set()
            broadcast_thread.join()
            self.tcp_socket.close()
            self.udp_socket.close()
            print("[Servidor] Finalizado.")

    def desligar(self):
        stop_event.set()
