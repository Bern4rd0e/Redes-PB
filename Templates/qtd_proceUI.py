import streamlit as st
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 5551))
s.listen(5)

class Qtd_proce:
    def main():
        st.header("Quantidade de processadores")

        clientesocket, address = s.accept()
        st.text(f"Conexão do endereço {address} foi ESTABELECIDA")

        msg = clientesocket.recv(12)

        st.text(f"Mensagem: {msg.decode('utf-8')}")

if __name__ == "__main__":
    Qtd_proce.main()