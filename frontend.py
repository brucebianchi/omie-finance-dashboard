import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Omie Finance Dashboard", layout="wide")

st.title("📊 Omie Finance Dashboard")
st.write("Dados financeiros obtidos via API Omie.")

# 🔗 Fazendo requisição ao backend FastAPI
API_URL = "https://<SEU_BACKEND_URL>/api/dados_financeiros"  # Substitua pela URL do seu backend

if st.button("🔄 Atualizar Dados"):
    response = requests.get(API_URL).json()

    saldo_total = response.get("contaCorrente", {}).get("vTotal", 0)
    contas_pagar_total = response.get("contaPagar", {}).get("vTotal", 0)
    contas_pagar_atraso = response.get("contaPagar", {}).get("vAtraso", 0)

    # 🎨 Função para criar os cartões
    def criar_cartao(cor_fundo, titulo, valor, subtitulo=""):
        width, height = 350, 130
        card = Image.new("RGB", (width, height), cor_fundo)
        draw = ImageDraw.Draw(card)

        def load_font(size):
            try:
                return ImageFont.truetype("arial.ttf", size)
            except:
                return ImageFont.load_default()

        font_title = load_font(24)
        font_value = load_font(28)
        font_subtitle = load_font(16)

        padding = 15
        draw.text((padding, 10), titulo, font=font_title, fill="white")
        valor_formatado = f"R$ {valor:,.2f}"
        draw.text((padding, 50), valor_formatado, font=font_value, fill="white")
        draw.text((padding, 90), subtitulo, font=font_subtitle, fill="white")

        return card

    # Criando os cartões
    cartao_saldo = criar_cartao("#E87432", "Saldo em Contas", saldo_total)
    cartao_pagar = criar_cartao("#D72638", "PAGAR HOJE", contas_pagar_total, f"Em atraso: R$ {contas_pagar_atraso:,.2f}")

    # Exibindo os cartões
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    axs[0].imshow(cartao_saldo)
    axs[0].axis("off")

    axs[1].imshow(cartao_pagar)
    axs[1].axis("off")

    st.pyplot(fig)
