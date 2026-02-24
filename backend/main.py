# backend/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.api.endpoints import alunos, chamada
from fastapi.responses import FileResponse
import os

# Inicializa o App
app = FastAPI(title="Chamadinha API Pro")

# Configurar CORS (Essencial para o frontend conseguir enviar dados)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Garante que a pasta de uploads existe para não dar erro no mount
os.makedirs("uploads", exist_ok=True)

# Servir as imagens salvas
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Evento que roda quando o servidor liga
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Incluir as rotas de lógica do sistema
app.include_router(alunos.router, tags=["Alunos"])
app.include_router(chamada.router, tags=["Chamada"])

# --- ROTAS DE NAVEGAÇÃO (FRONTEND) ---

@app.get("/")
async def pagina_inicial():
    """Ao acessar http://127.0.0.1:8000/, abre o login direto"""
    return FileResponse('../index.html')

@app.get("/login")
async def get_login():
    """Rota alternativa para /login"""
    return FileResponse('../index.html')

# --- ROTAS DE TESTE ---

@app.get("/status")
def status_api():
    return {"message": "Sistema Chamadinha Pro v1, rodando."}

@app.get("/teste-banco")
def teste():
    return {"status": "Tabelas verificadas no banco de dados."}