import streamlit as st
import threading
from servidor import Servidor, clientes_info, stop_event

class IndexUI:
    def iniciar_servidor():
        if 'server_thread' not in st.session_state or st.session_state['server_thread'] is None or not st.session_state['server_thread'].is_alive():
            stop_event.clear()
            servidor = Servidor()
            servidor.start()
            st.session_state['server_thread'] = servidor
            st.success("Servidor iniciado.")
        else:
            st.warning("Servidor já está rodando.")

    def desligar_servidor():
        if 'server_thread' in st.session_state and st.session_state['server_thread'] is not None:
            st.session_state['server_thread'].desligar()
            st.session_state['server_thread'].join(timeout=5)
            st.session_state['server_thread'] = None
            st.success("Servidor desligado.")
        else:
            st.warning("Servidor não está rodando.")

    def listar_clientes():
        return list(clientes_info.keys())

    def detalhar_cliente(ip):
        return clientes_info.get(ip, None)

    def calcular_media_ram():
        total_ram = 0
        count = 0
        for dados in clientes_info.values():
            try:
                total_ram += float(dados.get("ram_livre", 0))
                count += 1
            except:
                pass
        return total_ram / count if count else 0

    def formatar_detalhes_cliente(dados):
        linhas = []
        linhas.append(f"**Processadores:** {dados.get('processadores', 'N/A')}")
        linhas.append(f"**RAM Livre:** {dados.get('ram_livre', 'N/A')} GB")
        linhas.append(f"**Espaço em Disco Livre:** {dados.get('disco_livre', 'N/A')} GB")

        # Redes
        redes = dados.get("rede", {})
        redes_linhas = []
        for iface, info in redes.items():
            ips = ", ".join(info.get("ips", [])) or "Nenhum IP"
            status = info.get("status", "desconhecido")
            cor = "green" if status == "ativa" else "red"
            redes_linhas.append(f"- **{iface}** (<span style='color:{cor}'>{status}</span>): {ips}")
        redes_md = "\n".join(redes_linhas)
        linhas.append("**Interfaces de Rede:**\n" + redes_md)

        # Portas abertas
        portas = dados.get("portas_abertas", {})
        portas_tcp = ", ".join(str(p) for p in portas.get("tcp", [])) or "Nenhuma"
        portas_udp = ", ".join(str(p) for p in portas.get("udp", [])) or "Nenhuma"
        linhas.append(f"**Portas TCP abertas:** {portas_tcp}")
        linhas.append(f"**Portas UDP abertas:** {portas_udp}")

        return "\n\n".join(linhas)

    def main():
        st.set_page_config(page_title="Painel do Servidor", layout="wide")
        st.title("🖥️ Painel do Servidor - Monitoramento de Clientes")

        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Iniciar Servidor"):
                IndexUI.iniciar_servidor()
        with col2:
            if st.button("Desligar Servidor"):
                IndexUI.desligar_servidor()

        st.markdown("---")

        ips = IndexUI.listar_clientes()
        if ips:
            st.subheader("Clientes Conectados")
            st.write(f"Total de clientes: **{len(ips)}**")

            ip_selecionado = st.selectbox("Selecione um cliente para detalhar:", ips)
            if ip_selecionado:
                dados = IndexUI.detalhar_cliente(ip_selecionado)
                with st.expander(f"Detalhes do cliente {ip_selecionado}"):
                    st.markdown(IndexUI.formatar_detalhes_cliente(dados), unsafe_allow_html=True)
        else:
            st.info("Nenhum cliente conectado ainda.")

        st.markdown("---")

        if clientes_info:
            media_ram = IndexUI.calcular_media_ram()
            st.metric("Média de RAM livre dos clientes (GB)", f"{media_ram:.2f}")
        else:
            st.info("Nenhum dado para calcular média de RAM.")

if __name__ == "__main__":
    IndexUI.main()
