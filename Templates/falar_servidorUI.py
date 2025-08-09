import streamlit as st
import socket

class Falar_servidorUI:
    @staticmethod
    def main():
        st.header("Falar com Servidor")
        
        msg = st.text_area("Digite uma mensagem para o Servidor:")

        if "resposta" not in st.session_state:
            st.session_state.resposta = ""

        if st.button("Enviar"):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(("127.0.0.1", 5551))
                s.send(msg.encode('utf-8'))

                resposta = s.recv(4096)  # Recebe a resposta uma vez só

                s.close()
                st.success("Mensagem enviada ao servidor com sucesso!")
                st.session_state.resposta = resposta.decode('utf-8')

            except Exception as e:
                st.error(f"Erro: {e}")

        if st.session_state.resposta:
            st.text_area("Resposta do servidor:", st.session_state.resposta, height=150)

if __name__ == "__main__":
    Falar_servidorUI.main()
