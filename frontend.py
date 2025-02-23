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
    # 📌 Endpoints da API Omie
    url_resumo = "https://app.omie.com.br/api/v1/financas/resumo/"
    url_pagar = "https://app.omie.com.br/api/v1/financas/pesquisartitulos/"
    url_receber = "https://app.omie.com.br/api/v1/financas/pesquisartitulos/"

    # 📌 Payloads de requisição
    payload_resumo = {
        "call": "ObterResumoFinancas",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": [{"dDia": data_hoje, "lApenasResumo": True}]
    }

    payload_pagar = {
        "call": "ObterListaEmAberto",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": [{"dDia": data_hoje, "cTipo": "P", "nRegPorPagina": 50, "nPagina": 1}]
    }

    payload_receber = {
        "call": "ObterListaEmAberto",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": [{"dDia": data_hoje, "cTipo": "R", "nRegPorPagina": 50, "nPagina": 1}]
    }

    # 🔗 Chamadas para API da Omie
    response_resumo = requests.post(url_resumo, json=payload_resumo).json()
    response_pagar = requests.post(url_pagar, json=payload_pagar).json()
    response_receber = requests.post(url_receber, json=payload_receber).json()

    # 📌 Extraindo informações financeiras
    saldo_total = response_resumo.get("contaCorrente", {}).get("vTotal", 0)
    contas_pagar_total = response_resumo.get("contaPagar", {}).get("vTotal", 0)
    contas_pagar_atraso = response_resumo.get("contaPagar", {}).get("vAtraso", 0)
    contas_receber_total = response_resumo.get("contaReceber", {}).get("vTotal", 0)
    contas_receber_atraso = response_resumo.get("contaReceber", {}).get("vAtraso", 0)

    # 📌 Extração de categorias corrigida
    categorias_pagar = response_pagar.get("ListaEmEberto", [])
    categorias_receber = response_receber.get("ListaEmEberto", [])

    # 📌 Formatando categorias corretamente
    categorias_formatadas_pagar = [
        f"{cat.get('vDoc', 0):,.2f} {cat.get('cDescCateg', 'Sem descrição')}" for cat in categorias_pagar[:5]
    ] if categorias_pagar else ["Nenhuma categoria disponível"]

    categorias_formatadas_receber = [
        f"{cat.get('vDoc', 0):,.2f} {cat.get('cDescCateg', 'Sem descrição')}" for cat in categorias_receber[:5]
    ] if categorias_receber else ["Nenhuma categoria disponível"]

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
                <p style="font-size: 18px;">Em atraso: R$ {contas_receber_atraso:,.2f}</p>
                <div class="categories">{categorias_receber_texto}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
