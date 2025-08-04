import socket
import time

# Parâmetros de rede para a descoberta de clientes
HOST_BROADCAST = '255.255.255.255'  # Endereço de broadcast
PORT = 50000                      # Porta para o broadcast
MESSAGE = b'SOLICITACAO_DESCOBERTA' # Mensagem de requisição de descoberta

# Lista para armazenar os endereços IP dos clientes descobertos
clientes_descobertos = []

def iniciar_servidor_descoberta():
    """
    Inicia o servidor para enviar broadcast e descobrir clientes na rede.
    """
    print("Iniciando servidor de descoberta...")
    
    # Criação do socket UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Configura o socket para permitir broadcast
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Binda o socket a um endereço e porta. A porta é a mesma que o cliente irá ouvir.
    s.bind(('', PORT))
    
    print(f"Servidor de descoberta iniciado na porta {PORT}. Aguardando clientes...")
    
    try:
        s.settimeout(1) # Timeout curto para a espera por respostas
        
        # O servidor vai enviar o broadcast repetidamente
        for i in range(10): # Tenta 10 vezes
            print(f"Enviando broadcast ({i+1}/10): {MESSAGE.decode()}...")
            s.sendto(MESSAGE, (HOST_BROADCAST, PORT))
            time.sleep(3) # Espera 3 segundos antes de enviar de novo

            try:
                # O servidor irá esperar por respostas dos clientes
                data, addr = s.recvfrom(1024)
                
                if data == b'RESPOSTA_DESCOBERTA':
                    ip_cliente = addr[0]
                    if ip_cliente not in clientes_descobertos:
                        print(f"Cliente descoberto em: {ip_cliente}")
                        clientes_descobertos.append(ip_cliente)
                        
            except socket.timeout:
                continue # Continua o loop se não receber resposta
                
    except Exception as e:
        print(f"Erro no servidor de descoberta: {e}")
        
    finally:
        s.close()
        print("Servidor de descoberta finalizado.")
        
    if clientes_descobertos:
        print("\n--- Clientes Descobertos ---")
        for ip in clientes_descobertos:
            print(f"- {ip}")
    else:
        print("Nenhum cliente foi descoberto.")

# --- Execução do Código ---
if __name__ == "__main__":
    iniciar_servidor_descoberta()