from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode ser ajustado para maior segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Proxy para API da Omie
@app.post("/api/omie/{endpoint:path}")
async def proxy_omie(endpoint: str, request: Request):
    omie_url = f"https://app.omie.com.br/api/v1/{endpoint}"
    
    # Obtém o corpo da requisição
    data = await request.json()
    
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(omie_url, json=data, headers={"Content-Type": "application/json"})
        return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
