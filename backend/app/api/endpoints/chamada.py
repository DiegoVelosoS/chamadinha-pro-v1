# backend/app/api/endpoints/chamada.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Aluno
import face_recognition
import numpy as np
import json

router = APIRouter()

@router.post("/chamada/reconhecer")
async def reconhecer_alunos(
    foto: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    # 1. Carregar a foto enviada
    try:
        # Carrega a imagem direto da memória (sem salvar no disco para ser mais rápido)
        image = face_recognition.load_image_file(foto.file)
        # Encontra todos os rostos na foto (pode ter vários)
        rostos_desconhecidos = face_recognition.face_encodings(image)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao processar imagem")

    if not rostos_desconhecidos:
        return {"mensagem": "Nenhum rosto encontrado na foto.", "alunos_identificados": []}

    # 2. Buscar todos os alunos do banco
    alunos_banco = session.exec(select(Aluno)).all()
    
    # Preparar listas para o comparador
    nomes_conhecidos = []
    encodings_conhecidos = []
    ids_conhecidos = []

    for aluno in alunos_banco:
        if aluno.face_encoding_json:
            # Converte o JSON de volta para array numpy
            encoding = np.array(json.loads(aluno.face_encoding_json))
            encodings_conhecidos.append(encoding)
            nomes_conhecidos.append(aluno.nome)
            ids_conhecidos.append(aluno.id)

    if not encodings_conhecidos:
        return {"mensagem": "Nenhum aluno cadastrado no banco ainda.", "alunos_identificados": []}

    # 3. Comparar cada rosto da foto com o banco
    identificados = []

    for rosto_desconhecido in rostos_desconhecidos:
        # Compara com TODOS de uma vez (retorna lista de True/False)
        # tolerance=0.5 é a precisão (quanto menor, mais rigoroso)
        matches = face_recognition.compare_faces(encodings_conhecidos, rosto_desconhecido, tolerance=0.5)
        
        # Calcula a distância (quão parecido é) para pegar o melhor match
        face_distances = face_recognition.face_distance(encodings_conhecidos, rosto_desconhecido)
        
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            nome = nomes_conhecidos[best_match_index]
            aluno_id = ids_conhecidos[best_match_index]
            
            identificados.append({
                "id": aluno_id,
                "nome": nome,
                "confianca": float(1 - face_distances[best_match_index]) # Opcional: % de certeza
            })

    return {
        "total_rostos_na_foto": len(rostos_desconhecidos),
        "total_reconhecidos": len(identificados),
        "alunos": identificados
    }