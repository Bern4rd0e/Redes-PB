import streamlit as st
from Templates.qtd_proceUI import Qtd_proce

class IndexUI:
    @staticmethod
    def main():
        op = st.sidebar.selectbox("Insira um Comando: ",["Processadores", "Memória RAM Livre", "Espaço em disco livre", 
                                            "IP das Interfaces", "Interfaces Desativadas",
                                            "Portas TCP e UDP", "Dados consolidados",
                                            "Cliente"
                                            ])

        if op == "Processadores":
            Qtd_proce.main()



        
IndexUI.main()
