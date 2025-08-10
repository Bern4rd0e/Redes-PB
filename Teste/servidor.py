import socket
import psutil
import netifaces

class Servidor:
    def __init__(self, host="0.0.0.0", port=5551):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        print(f"Servidor iniciado em {self.host}:{self.port}")
        self.clientes_conectados = []  # Para armazenar dados dos clientes conectados
    
    def broadcast_discover(self, broadcast_port=5552):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        mensagem = b"DISCOVER_SERVER"
        udp.sendto(mensagem, ('<broadcast>', broadcast_port))
        udp.close()

    def listar_ips_interfaces(self):
        interfaces = netifaces.interfaces()
        resultado = []
        for iface in interfaces:
            addrs = netifaces.ifaddresses(iface)
            ip_info = addrs.get(netifaces.AF_INET, [{'addr': 'Sem IP'}])
            for ip in ip_info:
                resultado.append(f"{iface}: {ip['addr']}")
        return "\n".join(resultado)

    def interfaces_desativadas(self):
        stats = psutil.net_if_stats()
        desativadas = [iface for iface, st in stats.items() if not st.isup]
        if desativadas:
            return "Interfaces desativadas:\n" + "\n".join(desativadas)
        return "Nenhuma interface desativada."

    def listar_portas_abertas(self):
        conexoes = psutil.net_connections(kind='inet')
        portas = set()
        for c in conexoes:
            if c.status == 'LISTEN':
                proto = 'TCP' if c.type == socket.SOCK_STREAM else 'UDP'
                try:
                    proc_name = psutil.Process(c.pid).name() if c.pid else "Desconhecido"
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    proc_name = "Desconhecido"
                portas.add(f"{proto} {c.laddr.ip}:{c.laddr.port} - Processo: {proc_name} (PID {c.pid})")
        if portas:
            return "Portas abertas:\n" + "\n".join(portas)
        return "Nenhuma porta aberta."


    def media_simples_consolidada(self):
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        media = (cpu + (mem.percent) + (disk.percent)) / 3
        return (f"Média simples dos dados consolidados:\n"
                f"CPU: {cpu}%\n"
                f"RAM usada: {mem.percent}%\n"
                f"Disco usado: {disk.percent}%\n"
                f"Média: {media:.2f}%")

    def detalhar_cliente(self, endereco):
        # Como não temos histórico real, retornamos info simples do cliente
        return f"Detalhes do cliente:\nIP: {endereco[0]}\nPorta: {endereco[1]}"

    def main(self):
        running = True
        while running:
            try:
                clientsocket, address = self.s.accept()
                print(f"Conexão de {address} estabelecida.")
                self.clientes_conectados.append(address)

                msg = clientsocket.recv(1024)
                comando = msg.decode("utf-8").strip()
                print(f"Comando recebido: {comando}")

                if comando == "/help":
                    resposta = (
                        "Ajuda Requisitada:\n"
                        "\t/0 - Quantidade de Processadores\n"
                        "\t/1 - Ver memória RAM livre\n"
                        "\t/2 - Espaço em disco\n"
                        "\t/3 - Endereço IP das Interfaces\n"
                        "\t/4 - Mostrar Interfaces Desativadas\n"
                        "\t/6 - Listar portas TCP e UDP abertas\n"
                        "\t/7 - Mostrar média simples dos dados consolidados\n"
                        "\t/8 - Listar e detalhar último cliente conectado\n"
                        "\t/off - Desligar servidor"
                    )
                    clientsocket.send(resposta.encode("utf-8"))

                elif comando == "/0":
                    qtd = psutil.cpu_count(logical=True)
                    resposta = f"Quantidade de processadores: {qtd}"
                    clientsocket.send(resposta.encode("utf-8"))

                elif comando == "/1":
                    mem = psutil.virtual_memory()
                    resposta = (f"Memória RAM: total={mem.total/(1024**3):.2f} GB, "
                               f"disponível={mem.available/(1024**3):.2f} GB, "
                               f"usada={mem.used/(1024**3):.2f} GB")
                    clientsocket.send(resposta.encode("utf-8"))

                elif comando == "/2":
                    disk = psutil.disk_usage("/")
                    resposta = (f"Disco: total={disk.total/(1024**3):.2f} GB, "
                               f"usado={disk.used/(1024**3):.2f} GB, "
                               f"livre={disk.free/(1024**3):.2f} GB")
                    clientsocket.send(resposta.encode("utf-8"))

                elif comando == "/3":
                    resposta = self.listar_ips_interfaces()
                    clientsocket.send(resposta.encode("utf-8"))

                elif comando == "/4":
                    resposta = self.interfaces_desativadas()
                    clientsocket.send(resposta.encode("utf-8"))

                elif comando == "/6":
                    resposta = self.listar_portas_abertas()
                    clientsocket.send(resposta.encode("utf-8"))

                elif comando == "/7":
                    resposta = self.media_simples_consolidada()
                    clientsocket.send(resposta.encode("utf-8"))

                elif comando == "/8":
                    if self.clientes_conectados:
                        ultimo_cliente = self.clientes_conectados[-1]
                        resposta = self.detalhar_cliente(ultimo_cliente)
                    else:
                        resposta = "Nenhum cliente conectado ainda."
                    clientsocket.send(resposta.encode("utf-8"))

                elif comando == "/off":
                    resposta = "Desligando o servidor."
                    clientsocket.send(resposta.encode("utf-8"))
                    clientsocket.close()
                    running = False
                    break

                else:
                    resposta = "Comando inválido. Use /help para ajuda."
                    clientsocket.send(resposta.encode("utf-8"))

                clientsocket.close()

            except Exception as e:
                print(f"Erro: {e}")

        print("Servidor desligado.")
        self.s.close()


if __name__ == "__main__":
    try:
        import netifaces
    except ImportError:
        print("Instale o netifaces com 'pip install netifaces' para usar funcionalidades de IP")
        exit(1)

    servidor = Servidor()
    servidor.main()
