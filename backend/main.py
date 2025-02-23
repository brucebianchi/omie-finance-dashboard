import requests
import json
from PIL import Image, ImageDraw, ImageFont
import datetime
import matplotlib.pyplot as plt

# 🔑 Credenciais da API Omie (Substitua pelas suas credenciais)
app_key = "2875058458272"
app_secret = "5d3c695e3b2ef6dc1de57be4d3e7744b"

# 📅 Data de hoje
data_hoje = datetime.datetime.today().strftime('%d/%m/%Y')

# 📌 Endpoint para obter o resumo financeiro
url_resumo = "https://app.omie.com.br/api/v1/financas/resumo/"
payload_resumo = {
    "call": "ObterResumoFinancas",
    "app_key": app_key,
    "app_secret": app_secret,
    "param": [{"dDia": data_hoje, "lApenasResumo": True}]
}

# 📌 Endpoint para obter contas a pagar
url_pagar = "https://app.omie.com.br/api/v1/financas/pesquisartitulos/"
payload_pagar = {
    "call": "ObterListaEmAberto",
    "app_key": app_key,
    "app_secret": app_secret,
    "param": [{"dDia": data_hoje, "cTipo": "P", "nRegPorPagina": 50, "nPagina": 1}]
}

# 🔗 Fazendo as requisições para a API Omie
response_resumo = requests.post(url_resumo, json=payload_resumo).json()
response_pagar = requests.post(url_pagar, json=payload_pagar).json()

# 📌 Extração de dados do saldo em contas
saldo_total = response_resumo.get("contaCorrente", {}).get("vTotal", 0)

# 📌 Extração de dados das contas a pagar
contas_pagar_total = response_resumo.get("contaPagar", {}).get("vTotal", 0)
contas_pagar_atraso = response_resumo.get("contaPagar", {}).get("vAtraso", 0)
categorias_pagar = response_resumo.get("contaPagarCategoria", [])

# 📌 Garantir que categorias_pagar é uma lista válida
if categorias_pagar is None:
    categorias_pagar = []

# 📌 Criando um resumo das categorias de contas a pagar
categorias_texto = []
for categoria in categorias_pagar[:5]:  # Limita a 5 categorias para melhor legibilidade
    categoria_valor = categoria.get('vTotal', 0)
    categoria_desc = categoria.get('cDescCateg', 'Sem descrição')
    categorias_texto.append(f"{categoria_valor:,.2f} {categoria_desc}")

# 🎨 Função para criar os cartões
def criar_cartao(cor_fundo, titulo, valor, subtitulo="", categorias=[]):
    width, height = 350, 130  # **Ajustado para melhor leitura**
    card = Image.new("RGB", (width, height), cor_fundo)
    draw = ImageDraw.Draw(card)

    # 🔹 Melhor abordagem para fontes escaláveis
    def load_font(size):
        try:
            return ImageFont.truetype("arial.ttf", size)
        except:
            return ImageFont.load_default()

    # 🔹 Tamanhos ajustados proporcionalmente ao cartão
    font_title = load_font(30)  # Título
    font_value = load_font(28)  # Valor
    font_subtitle = load_font(18)  # Subtítulo menor
    font_categories = load_font(14)  # Fonte menor para categorias

    # 📌 Margens e espaçamentos
    padding = 15
    espacamento = 5

    # 📌 Título
    draw.text((padding, espacamento), titulo, font=font_title, fill="white")

    # 📌 Valor principal
    valor_formatado = f"R$ {valor:,.2f}"
    draw.text((padding, 50), valor_formatado, font=font_value, fill="white")

    # 📌 Subtítulo
    draw.text((padding, 85), subtitulo, font=font_subtitle, fill="white")

    # 📌 Categorias (se houver)
    y_categoria = 105
    for categoria in categorias:
        draw.text((padding, y_categoria), categoria, font=font_categories, fill="white")
        y_categoria += 18  # Incrementa para a próxima linha

    return card

# 📌 Criando os cartões
cartao_saldo = criar_cartao("#E87432", "Saldo em Contas", saldo_total)
cartao_pagar = criar_cartao("#D72638", "PAGAR HOJE", contas_pagar_total, f"sendo em atraso R$ {contas_pagar_atraso:,.2f}", categorias_texto)

# 📌 Exibir os cartões no Google Colab
fig, axs = plt.subplots(1, 2, figsize=(14, 5))

axs[0].imshow(cartao_saldo)
axs[0].axis("off")  # Oculta os eixos

axs[1].imshow(cartao_pagar)
axs[1].axis("off")  # Oculta os eixos

plt.show()
