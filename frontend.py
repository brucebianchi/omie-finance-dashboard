import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import datetime
import matplotlib.pyplot as plt

# 🔑 Credenciais da API Omie (coloque suas credenciais reais)
APP_KEY = "2875058458272"
APP_SECRET = "5d3c695e3b2ef6dc1de57be4d3e7744b"

# 📅 Data de hoje
data_hoje = datetime.datetime.today().strftime('%d/%m/%Y')

# 🎨 Função para criar os cartões gráficos
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

# 🔗 Fazendo requisição para API Omie diretamente no Streamlit
st.title("📊 Omie Finance Dashboard")
st.write("Dados financeiros obtidos via API Omie.")

if st.button("🔄 Atualizar Dados"):
    # 🔗 Endpoint para obter resumo financeiro
    url_resumo = "https://app.omie.com.br/api/v1/financas/resumo/"
    payload_resumo = {
        "call": "ObterResumoFinancas",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": [{"dDia": data_hoje, "lApenasResumo": True}]
    }

    response = requests.post(url_resumo, json=payload_resumo).json()

    saldo_total = response.get("contaCorrente", {}).get("vTotal", 0)
    contas_pagar_total = response.get("contaPagar", {}).get("vTotal", 0)
    contas_pagar_atraso = response.get("contaPagar", {}).get("vAtraso", 0)

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
