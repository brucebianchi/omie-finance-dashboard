import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Omie Finance Dashboard", layout="wide")

st.title("📊 Gerador de Demonstrações Financeiras")
st.write("Insira os dados e gere relatórios automaticamente com a API da Omie.")

# Entrada do usuário
endpoint = st.text_input("Digite o endpoint da Omie (exemplo: /financas/contas)")
data = st.text_area("Digite o JSON da requisição", "{}")

if st.button("Enviar para API"):
    try:
        response = requests.post(f"http://127.0.0.1:8000/api/omie{endpoint}", json=eval(data))
        st.json(response.json())
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {str(e)}")

