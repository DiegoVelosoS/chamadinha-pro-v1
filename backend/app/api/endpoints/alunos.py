from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Aluno
import face_recognition
import shutil
import os
import json
import csv

router = APIRouter()

# Local onde estão as imagens
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
CSV_PATH = "./alunos.csv"

@router.post("/alunos/", response_model=Aluno)
async def criar_aluno(
    nome: str = Form(...),
    whatsapp: str = Form(None),
    turma: str = Form("Adulto Noite"),
    foto: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    # 1. Definir o caminho do arquivo de imagem
    file_location = f"{UPLOAD_DIR}/{foto.filename}"
    
    # 2. Salvar o arquivo no disco
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(foto.file, buffer)

    # 3. Processar a IA (Face Recognition)
    try:
        image = face_recognition.load_image_file(file_location)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            if os.path.exists(file_location):
                os.remove(file_location)
            raise HTTPException(status_code=400, detail="Nenhum rosto detectado na foto!")
        
        face_encoding = encodings[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar imagem: {str(e)}")

    # 4. Criar o objeto Aluno e Salvar no Banco de Dados (SQLite)
    novo_aluno = Aluno(
        nome=nome,
        whatsapp=whatsapp,
        turma=turma,
        foto_url=file_location
    )
    novo_aluno.set_encoding(face_encoding.tolist())

    session.add(novo_aluno)
    session.commit()
    session.refresh(novo_aluno)

    # 5. Salvar também no CSV (Mantendo a lógica que você tinha antes)
    manter_registro_csv(novo_aluno)
    
    return novo_aluno

def manter_registro_csv(aluno: Aluno):
    """Função auxiliar para salvar os dados no CSV em formato Python"""
    file_exists = os.path.isfile(CSV_PATH)
    
    with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "ID", "NOME", "WHATSAPP", "TURMA", "DATA_CADASTRO"
        ])
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            "ID": aluno.id,
            "NOME": aluno.nome,
            "WHATSAPP": aluno.whatsapp,
            "TURMA": aluno.turma,
            "DATA_CADASTRO": aluno.data_cadastro.strftime("%d/%m/%Y %H:%M")
        })

@router.get("/alunos/", response_model=list[Aluno])
def listar_alunos(session: Session = Depends(get_session)):
    alunos = session.exec(select(Aluno)).all()
    return alunos