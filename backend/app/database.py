# backend/app/database.py
from sqlmodel import SQLModel, create_engine, Session

# Nome do arquivo do banco. Futuramente, aqui entra a URL do PostgreSQL.
DATABASE_URL = "sqlite:///./chamadinha.db"

# connect_args é necessário apenas para SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Cria as tabelas no banco se elas não existirem"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependência para injetar a sessão do banco nas rotas"""
    with Session(engine) as session:
        yield session