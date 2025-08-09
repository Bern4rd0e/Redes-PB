import socket

class Cliente:
    def __init__(self, host="127.0.0.1", port=5551):
        self.host = host
        self.port = port
        self.sock = None

    def conectar(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def enviar_comando(self, comando):
        if not self.sock:
            raise RuntimeError("Cliente não conectado")
        self.sock.sendall(comando.encode('utf-8'))
        
        resposta = b""
        self.sock.settimeout(2)
        try:
            while True:
                parte = self.sock.recv(4096)
                if not parte:
                    break
                resposta += parte
        except socket.timeout:
            pass
        return resposta.decode('utf-8')

    def fechar(self):
        if self.sock:
            self.sock.close()
            self.sock = None

if __name__ == "__main__":
    cliente = Cliente()
    try:
        cliente.conectar()

        comandos = ["QtdProcessadores", "RamLivre", "OutroComando"]  # Lista dos comandos que quer enviar
        for cmd in comandos:
            resposta = cliente.enviar_comando(cmd)
            print(f"Comando: {cmd} -> Resposta: {resposta}")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        cliente.fechar()
