import streamlit as st
from Models.cliente import Cliente
from Templates.falar_servidorUI import Falar_servidorUI
from Templates.qtd_proceUI import Qtd_proceUI
from Templates.ramUI import RamUI

class IndexUI:
    @staticmethod
    def main():
        op = st.sidebar.selectbox("Insira um Comando: ",[
            "Falar com Servidor",
            "Processadores",
            "Memória RAM Livre",
            "Espaço em disco livre", 
            "IP das Interfaces", 
            "Interfaces Desativadas",
            "Portas TCP e UDP", 
            "Dados consolidados",
            "Cliente"
        ])

        if op == "Falar com Servidor":
            Falar_servidorUI.main()

        if op == "Processadores":
            Qtd_proceUI.main()
        
        if op == "Memória RAM Livre":
            RamUI.main()

        elif op == "Cliente":
            st.header("Cliente - Conectando ao servidor")
            cli = Cliente()
            try:
                cli.conectar()
                comando = st.text_input("Digite o comando para enviar ao servidor:", value="qtd_proce")
                if st.button("Enviar comando"):
                    resposta = cli.enviar_comando(comando)
                    st.write("Resposta do servidor:")
                    st.code(resposta)
                cli.fechar()
            except Exception as e:
                st.error(f"Erro ao conectar ou comunicar: {e}")

IndexUI.main()
