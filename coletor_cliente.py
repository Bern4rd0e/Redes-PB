import psutil
import socket
import json

class ColetorDadosSistema: 
    """
    Classe responsável por coletar o que foi pedido
    """
    def __init__(self):
        # O construtor é o lugar ideal para inicializar o objeto,
        # mas para este exemplo, não precisamos de nada.
        pass

    def obter_informacoes_processador(self): # (0,5) - Quantidade de Processadores
        """Retorna a quantidade de processadores (núcleos lógicos)."""
        return psutil.cpu_count(logical=True)

    def obter_informacoes_ram_livre(self): # (0,5) - Memória RAM Livre: A função obter_informacoes_ram_livre() faz esse trabalho.
        """Retorna a memória RAM livre em GB, formatado para duas casas decimais."""
        memoria = psutil.virtual_memory()
        ram_livre_gb = memoria.available / (1024**3)
        return f"{ram_livre_gb:.2f}"

    def obter_espaco_disco_livre(self): #  (0,5) - Espaço em disco livre
        """Retorna o espaço em disco livre na partição principal em GB, formatado para duas casas decimais."""
        try:
            disco = psutil.disk_usage('/')  # Para sistemas tipo Unix (Linux, macOS)
        except FileNotFoundError:
            disco = psutil.disk_usage('C:')  # Para Windows
            
        espaco_livre_gb = disco.free / (1024**3)
        return f"{espaco_livre_gb:.2f}"

    def obter_informacoes_rede(self): # (0,5) - Endereço IP das Interfaces
        """
        Retorna informações de rede, incluindo IPs, e status das interfaces (ativas/desativadas).
        """
        interfaces_info = {}
        # Obtém endereços IP e nome das interfaces
        adresses = psutil.net_if_addrs()
        # Obtém o status (ativo/desativado)
        stats = psutil.net_if_stats()

        for interface_nome, addrs in adresses.items():
            ips = [addr.address for addr in addrs if addr.family == socket.AF_INET]
            status = "ativada" if stats[interface_nome].isup else "desativada"
            interfaces_info[interface_nome] = {
                "ips": ips,
                "status": status
            }

        # Adiciona interfaces desativadas que não têm endereço IP (psutil.net_if_addrs() não as lista)
        for interface_nome, interface_stats in stats.items():
            if not interface_stats.isup and interface_nome not in interfaces_info:
                interfaces_info[interface_nome] = {
                    "ips": [],
                    "status": "desativada"
                }

        return interfaces_info

    def obter_portas_abertas(self): # (0,5) - Listar portas TCP e UDP abertas 
        """
        Lista as portas TCP e UDP em estado de "LISTEN".
        """
        portas = {"tcp": [], "udp": []}
        for conexao in psutil.net_connections(kind='inet'):
            if conexao.status == "LISTEN":
                if conexao.type == socket.SOCK_STREAM:  # TCP
                    portas["tcp"].append(conexao.laddr.port)
                elif conexao.type == socket.SOCK_DGRAM:  # UDP
                    portas["udp"].append(conexao.laddr.port)
        return portas
    
    def coletar_todos_os_dados(self):
        """
        Coleta todos os dados e os retorna em um único dicionário.
        """
        dados = {
            "processadores": self.obter_informacoes_processador(),
            "ram_livre": self.obter_informacoes_ram_livre(),
            "disco_livre": self.obter_espaco_disco_livre(),
            "rede": self.obter_informacoes_rede(),
            "portas_abertas": self.obter_portas_abertas()
        }
        return dados


# --- Execução do Código Principal ---
if __name__ == "__main__":
    # Parâmetros de rede para a descoberta
    HOST_BROADCAST = ''
    PORT = 50000
    MESSAGE = b'SOLICITACAO_DESCOBERTA'
    RESPONSE = b'RESPOSTA_DESCOBERTA'

    # Criação do socket UDP para ouvir o broadcast do servidor
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST_BROADCAST, PORT))

    print("Cliente de descoberta iniciado. Aguardando broadcast do servidor...")

    try:
        s.settimeout(30) # Define um tempo limite para esperar pelo broadcast
        data, addr = s.recvfrom(1024)
        if data == MESSAGE:
            ip_servidor = addr[0]
            print(f"Broadcast do servidor recebido de: {ip_servidor}")
            
            # Responde ao servidor com uma mensagem de confirmação
            s.sendto(RESPONSE, (ip_servidor, PORT))
            print("Resposta enviada para o servidor.")

            # Coleta e exibe os dados (opcional para o teste)
            coletor = ColetorDadosSistema()
            dados_coletados = coletor.coletar_todos_os_dados()
            print("\n--- Dados Coletados ---")
            print(json.dumps(dados_coletados, indent=4))
        
    except socket.timeout:
        print("Tempo limite de espera pelo broadcast esgotado. Servidor não encontrado.")
    except Exception as e:
        print(f"Erro no cliente: {e}")
    finally:
        s.close()