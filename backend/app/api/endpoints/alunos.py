# backend/app/api/endpoints/alunos.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Aluno
import face_recognition
import shutil
import os
import json

router = APIRouter()

# Local onde salvaremos as imagens
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/alunos/", response_model=Aluno)
async def criar_aluno(
    nome: str = Form(...),
    whatsapp: str = Form(None),
    turma: str = Form("Adulto Noite"),
    foto: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    # 1. Definir o caminho do arquivo
    file_location = f"{UPLOAD_DIR}/{foto.filename}"
    
    # 2. Salvar o arquivo no disco
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(foto.file, buffer)

    # 3. Processar a IA (Face Recognition)
    try:
        # Carrega a imagem salva
        image = face_recognition.load_image_file(file_location)
        # Tenta encontrar rostos
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            # Apaga a foto se não tiver rosto para não sujar o servidor
            os.remove(file_location)
            raise HTTPException(status_code=400, detail="Nenhum rosto detectado na foto!")
        
        # Pega o primeiro rosto encontrado
        face_encoding = encodings[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar imagem: {str(e)}")

    # 4. Criar o objeto Aluno e Salvar no Banco
    novo_aluno = Aluno(
        nome=nome,
        whatsapp=whatsapp,
        turma=turma,
        foto_url=file_location
    )
    # Converte o array numpy para lista e salva como JSON
    novo_aluno.set_encoding(face_encoding.tolist())

    session.add(novo_aluno)
    session.commit()
    session.refresh(novo_aluno)
    
    return novo_aluno

@router.get("/alunos/", response_model=list[Aluno])
def listar_alunos(session: Session = Depends(get_session)):
    alunos = session.exec(select(Aluno)).all()
    return alunos

# Rota para exportar alunos para CSV
const express = require('express');
const fs = require('fs');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const router = express.Router();

const csvPath = './alunos.csv';

const csvWriter = createCsvWriter({
  path: csvPath,
  header: [
    {id: 'N', title: 'Nº'},
    {id: 'QTD', title: 'QTD'},
    {id: 'COD', title: 'COD'},
    {id: 'CATEGORIA', title: 'CATEGORIA'},
    {id: 'NOME', title: 'NOME'},
    {id: 'SOBRENOME', title: 'SOBRENOME'},
    {id: 'DT_NASC', title: 'DT.NASC'},
    {id: 'DT_MAT', title: 'DT.MAT'},
    {id: 'STATUS', title: 'STATUS'},
    {id: 'TURNO', title: 'TURNO'},
    {id: 'PLANO', title: 'PLANO'},
    {id: 'CONTATO', title: 'CONTATO'},
    {id: 'USER_CAD', title: 'USER.CAD'},
  ],
  append: true
});

router.post('/cadastro', async (req, res) => {
  const aluno = req.body;

  // Lê todos os alunos para calcular Nº e QTD
  let alunos = [];
  if (fs.existsSync(csvPath)) {
    const data = fs.readFileSync(csvPath, 'utf8');
    alunos = data.split('\n').slice(1).filter(Boolean).map(l => l.split(','));
  }
  const N = alunos.length + 1;
  const QTD = alunos.filter(a => a[3] === aluno.CATEGORIA).length + 1;
  const COD = aluno.CATEGORIA + QTD;

  await csvWriter.writeRecords([{
    N,
    QTD,
    COD,
    CATEGORIA: aluno.CATEGORIA,
    NOME: aluno.NOME,
    SOBRENOME: aluno.SOBRENOME,
    DT_NASC: aluno.DT_NASC,
    DT_MAT: aluno.DT_MAT,
    STATUS: aluno.STATUS,
    TURNO: aluno.TURNO,
    PLANO: aluno.PLANO,
    CONTATO: aluno.CONTATO,
    USER_CAD: aluno.USER_CAD
  }]);

  res.json({ success: true, COD });
});

module.exports = router;
