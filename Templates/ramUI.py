import streamlit as st
import socket
import psutil

class RamUI:
    @staticmethod
    def main():
        st.header("Memória RAM livre")

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", 5551))
            s.send("RamLivre".encode('utf-8'))

            resposta = s.recv(1024)
            s.close()

            memoria = psutil.virtual_memory()
            ram_livre_gb = memoria.available / (1024**3)
            return f"{ram_livre_gb:.2f}"
        except Exception as e:
            st.error(f"Erro: {e}")

if __name__ == "__main__":
    RamUI.main()
