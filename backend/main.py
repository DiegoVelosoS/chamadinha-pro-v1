# backend/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.database import create_db_and_tables
from app.models import Aluno
from app.api.endpoints import alunos, chamada



# Inicializa o App
app = FastAPI(title="Chamadinha API Pro")

# Configurar CORS (Permite que o React converse com o Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o que está "*" é o domínio do site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar para servir as imagens salvas (para o frontend ver depois)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Evento que roda quando o servidor liga
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Incluir as rotas de alunos
app.include_router(alunos.router, tags=["Alunos"])
app.include_router(chamada.router, tags=["Chamada"])

@app.get("/")
def read_root():
    return {"message": "Sistema Chamadinha Pro v1, rodando."}

# Rota de teste para ver se o banco está respondendo (apenas exemplo)
@app.get("/teste-banco")
def teste():
    return {"status": "Tabelas criadas no chamadinha.db"}