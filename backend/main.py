from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn
import datetime

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode ser ajustado para maior segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Credenciais da API Omie
APP_KEY = "2875058458272"
APP_SECRET = "5d3c695e3b2ef6dc1de57be4d3e7744b"

# Proxy para API da Omie
@app.post("/api/omie/{endpoint:path}")
async def proxy_omie(endpoint: str, request: Request):
    omie_url = f"https://app.omie.com.br/api/v1/{endpoint}"
    
    # Obtém o corpo da requisição
    data = await request.json()
    
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(omie_url, json=data, headers={"Content-Type": "application/json"})
        
        # Verifica se houve erro na resposta do Omie
        response_json = response.json()
        if "faultstring" in response_json or "faultcode" in response_json:
            return {"error": "Erro na API do Omie", "details": response_json.get("faultstring", "Erro desconhecido")}, 400
        
        return response_json

@app.get("/api/dados_financeiros")
async def obter_dados_financeiros():
    data_hoje = datetime.datetime.today().strftime('%d/%m/%Y')
    
    payload_resumo = {
        "call": "ObterResumoFinancas",
        "app_key": APP_KEY,
        "app_secret": APP_SECRET,
        "param": [{"dDia": data_hoje, "lApenasResumo": True}]
    }
    
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post("https://app.omie.com.br/api/v1/financas/resumo/", json=payload_resumo)
        resumo_data = response.json()
        
        # Pegando categorias das contas a pagar e a receber
        categorias_pagar = resumo_data.get("contaPagarCategoria", [])
        categorias_receber = resumo_data.get("contaReceberCategoria", [])
        
        # Formatar categorias
        categorias_formatadas_pagar = [
            {"categoria": cat.get("cDescCateg", "Sem descrição"), "valor": cat.get("vTotal", 0)}
            for cat in categorias_pagar
        ]
        
        categorias_formatadas_receber = [
            {"categoria": cat.get("cDescCateg", "Sem descrição"), "valor": cat.get("vTotal", 0)}
            for cat in categorias_receber
        ]
        
        resumo_data["categorias_pagar"] = categorias_formatadas_pagar
        resumo_data["categorias_receber"] = categorias_formatadas_receber
        
        return resumo_data

@app.get("/")
def home():
    return {"message": "Servidor FastAPI rodando!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
