# backend/app/models.py
from typing import Optional, List
from sqlmodel import SQLModel, Field
from datetime import datetime
import json

class AlunoBase(SQLModel):
    nome: str
    whatsapp: Optional[str] = None
    turma: str = "Adulto Noite"
    foto_url: Optional[str] = None # Caminho da foto salva em disco
    status_pagamento: str = "Pendente"

class Aluno(AlunoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_cadastro: datetime = Field(default_factory=datetime.now)
    
    # O "segredo" da IA: Armazenamos o vetor de 128 números como uma String JSON
    face_encoding_json: str = Field(default="[]") 

    # Helpers para converter de/para lista Python automaticamente
    def set_encoding(self, encoding_list):
        self.face_encoding_json = json.dumps(encoding_list)

    def get_encoding(self):
        return json.loads(self.face_encoding_json)

# Aqui você pode adicionar as classes Financeiro e Presenca depois