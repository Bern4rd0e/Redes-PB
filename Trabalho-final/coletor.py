import psutil
import socket

# Chave AES de 16 bytes (AES-128) — altere para uma chave secreta sua, com 16 bytes exatos
chave = b'minha-chave-1234'  # EXATAMENTE 16 bytes

class ColetorDadosSistema:
    def __init__(self):
        pass

    def obter_informacoes_processador(self):
        return psutil.cpu_count(logical=True)

    def obter_informacoes_ram_livre(self):
        memoria = psutil.virtual_memory()
        ram_gb = memoria.available / (1024**3)
        return f"{ram_gb:.2f}"

    def obter_espaco_disco_livre(self):
        try:
            disco = psutil.disk_usage('/')
        except FileNotFoundError:
            disco = psutil.disk_usage('C:')
        livre_gb = disco.free / (1024**3)
        return f"{livre_gb:.2f}"

    def obter_informacoes_rede(self):
        interfaces_info = {}
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        for iface, addrs_list in addrs.items():
            ips = [a.address for a in addrs_list if a.family == socket.AF_INET]
            status = "ativa" if stats[iface].isup else "desativada"
            interfaces_info[iface] = {
                "ips": ips,
                "status": status
            }
        return interfaces_info

    def obter_portas_abertas(self):
        portas = {"tcp": [], "udp": []}
        for conexao in psutil.net_connections(kind='inet'):
            if conexao.status == "LISTEN":
                if conexao.type == socket.SOCK_STREAM:
                    portas["tcp"].append(conexao.laddr.port)
                elif conexao.type == socket.SOCK_DGRAM:
                    portas["udp"].append(conexao.laddr.port)
        return portas

    def coletar_todos_os_dados(self):
        return {
            "processadores": self.obter_informacoes_processador(),
            "ram_livre": self.obter_informacoes_ram_livre(),
            "disco_livre": self.obter_espaco_disco_livre(),
            "rede": self.obter_informacoes_rede(),
            "portas_abertas": self.obter_portas_abertas()
        }
