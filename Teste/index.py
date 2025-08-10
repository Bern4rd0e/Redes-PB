import streamlit as st
from cliente import Cliente

class IndexUI:
    @staticmethod
    def main():
        st.header("Escolha um comando para enviar ao servidor")

        server_ip = st.text_input("IP do servidor:", "127.0.0.1")

        comandos_dict = {
            "Ajuda": "/help",
            "Quantidade de Processadores": "/0",
            "Ver memória RAM livre": "/1",
            "Ver espaço em disco": "/2",
            "Listar IP das interfaces": "/3",
            "Mostrar interfaces desativadas": "/4",
            "Listar portas TCP e UDP abertas": "/6",
            "Mostrar média simples dos dados consolidados": "/7",
            "Listar e detalhar último cliente conectado": "/8",
            "Desligar servidor": "/off"
        }

        nomes_comandos = list(comandos_dict.keys())
        comando_selecionado = st.selectbox("Selecione o comando:", nomes_comandos, index=1)

        if st.button("Enviar comando"):
            cli = Cliente(server_ip)
            try:
                with st.spinner("Conectando ao servidor..."):
                    cli.conectar()
                    resposta = cli.enviar_comando(comandos_dict[comando_selecionado])
                st.success("Comando enviado com sucesso!")
                st.text_area("Resposta do servidor:", resposta, height=300)
            except Exception as e:
                

if __name__ == "__main__":
    IndexUI.main()
