import streamlit as st
import requests
import datetime

# 🔑 Credenciais da API Omie
APP_KEY = "2875058458272"
APP_SECRET = "5d3c695e3b2ef6dc1de57be4d3e7744b"

# 📅 Data de hoje
data_hoje = datetime.datetime.today().strftime('%d/%m/%Y')

# 🎨 Estilização CSS personalizada
st.markdown("""
    <style>
        .card {
            padding: 20px;
            border-radius: 10px;
            text-align: left;
            color: white;
            font-family: Arial, sans-serif;
            font-size: 20px;
            margin-bottom: 20px;
        }
        .card-orange { background-color: #E87432; }
        .card-red { background-color: #D72638; }
        .card-blue { background-color: #1E90FF; }
        .container {
            display: flex;
            justify-content: space-between;
        }
        .box {
            width: 30%;
            padding: 10px;
        }
        .categories {
            font-size: 16px;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 🔗 Fazendo requisição para API Omie diretamente
st.title("📊 Omie Finance Dashboard")
st.write("Dados financeiros obtidos via API Omie.")

if st.button("🔄 Atualizar Dados"):
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
    contas_receber_total = response.get("contaReceber", {}).get("vTotal", 0)

    categorias_pagar = response.get("contaPagarCategoria", [])
    categorias_receber = response.get("contaReceberCategoria", [])

    # Formatar categorias
    categorias_formatadas_pagar = [
        f"{cat.get('vTotal', 0):,.2f} {cat.get('cDescCateg', 'Sem descrição')}" for cat in categorias_pagar[:5]
    ]
    categorias_formatadas_receber = [
        f"{cat.get('vTotal', 0):,.2f} {cat.get('cDescCateg', 'Sem descrição')}" for cat in categorias_receber[:5]
    ]

    # 📌 Melhor organização dos cartões
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # 💰 Saldo em Contas
    st.markdown(f"""
        <div class="box">
            <div class="card card-orange">
                <h3>💰 Saldo em Contas</h3>
                <p style="font-size: 28px;"><b>R$ {saldo_total:,.2f}</b></p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 📉 Contas a Pagar
    categorias_pagar_texto = "<br>".join(categorias_formatadas_pagar)
    st.markdown(f"""
        <div class="box">
            <div class="card card-red">
                <h3>📉 PAGAR HOJE</h3>
                <p style="font-size: 28px;"><b>R$ {contas_pagar_total:,.2f}</b></p>
                <p style="font-size: 18px;">Em atraso: R$ {contas_pagar_atraso:,.2f}</p>
                <div class="categories">{categorias_pagar_texto}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 📈 Contas a Receber
    categorias_receber_texto = "<br>".join(categorias_formatadas_receber)
    st.markdown(f"""
        <div class="box">
            <div class="card card-blue">
                <h3>📈 RECEBER HOJE</h3>
                <p style="font-size: 28px;"><b>R$ {contas_receber_total:,.2f}</b></p>
                <div class="categories">{categorias_receber_texto}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
