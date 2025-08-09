import socket
import threading
import psutil

class Servidor:
    def __init__(self, host="0.0.0.0", port=5551):
        self.host = host
        self.port = port
        self.clientes = []

    def tratar_cliente(self, clientesocket, address):
        print(f"Cliente {address} conectado.")
        self.clientes.append(clientesocket)

        try:
            while True:
                msg = clientesocket.recv(1024)
                if not msg:
                    break
                texto = msg.decode('utf-8').strip()
                print(f"Recebido de {address}: {texto}")

                # Responde com dados ou eco
                if texto == "QtdProcessadores":
                    qtd = psutil.cpu_count(logical=True)
                    clientesocket.send(str(qtd).encode('utf-8'))

                elif texto == "RamLivre":
                    memoria = psutil.virtual_memory()
                    ram_livre_gb = memoria.available / (1024**3)
                    return f"{ram_livre_gb:.2f}"
                else:
                    clientesocket.send(f"Eco: {texto}".encode('utf-8'))

        finally:
            clientesocket.close()
            self.clientes.remove(clientesocket)
            print(f"Cliente {address} desconectado.")

    def iniciar_servidor(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        print(f"Servidor iniciado na porta {self.port}")

        while True:
            clientesocket, address = s.accept()
            thread = threading.Thread(target=self.tratar_cliente, args=(clientesocket, address))
            thread.start()

if __name__ == "__main__":
    servidor = Servidor()
    servidor.iniciar_servidor()
