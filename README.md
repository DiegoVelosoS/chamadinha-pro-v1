# Chamadinha Pro v1 (descontinuado)

> Primeira versão do sistema **Chamadinha Pro** (descontinuada), focada em **controle de presença (chamada)** com **reconhecimento facial**.

O projeto é dividido em dois módulos:
- **Backend** (Python/FastAPI): API + banco de dados + reconhecimento facial
- **Frontend** (React/Vite): interface web para login e painel de chamada

---

## O que este sistema faz

- Cadastro de alunos com:
  - Nome, whatsapp, turma, status de pagamento
  - Upload de foto do aluno (salva em disco)
  - Extração do **encoding facial** (vetor numérico) usando a lib `face_recognition`
- Chamada por foto:
  - Envio de uma foto (por exemplo, foto da turma)
  - Detecção de rostos e comparação com os alunos cadastrados
  - Retorno com lista de alunos reconhecidos e “confiança” aproximada

---

## Arquitetura

### Frontend (`/frontend`)
- React + Vite
- Rotas:
  - `/` → Login (simples / demonstrativo)
  - `/painel` → Painel com botão para capturar/enviar imagem
- Comunicação com o backend via HTTP:
  - `POST http://127.0.0.1:8000/chamada/reconhecer`

### Backend (`/backend`)
- FastAPI (`backend/main.py`)
- Banco: SQLite (`backend/chamadinha.db`)
- ORM: SQLModel
- Uploads: imagens salvas em `backend/uploads/`
- Reconhecimento facial:
  - Cadastro: extrai encoding e armazena no banco como JSON string
  - Chamada: compara encodings com `compare_faces` + `face_distance`

---

## Tecnologias

### Backend
- Python
- FastAPI
- Uvicorn
- SQLModel + SQLite
- face_recognition
- numpy
- python-multipart

### Frontend
- JavaScript
- React
- Vite
- react-router-dom
- lucide-react

---

## Como iniciar o sistema (modo desenvolvimento)

### 1) Backend

Requisitos:
- Python 3.10+ (recomendado)
- Dependências nativas para `face_recognition` (ex.: `cmake` e libs do `dlib`, variam por SO)

Passos:

```bash
cd backend

python -m venv .venv
# Windows:
# .venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload --port 8000
```

API online em:
- http://127.0.0.1:8000
- Swagger/OpenAPI:
  - http://127.0.0.1:8000/docs

### 2) Frontend

Requisitos:
- Node.js 18+ (recomendado)

Passos:

```bash
cd frontend
npm install
npm run dev
```

Aplicação em:
- http://127.0.0.1:5173 (porta padrão do Vite, pode variar)

---

## Endpoints principais (Backend)

- `GET /status`  
  Retorna status simples da API.

- `POST /alunos/`  
  Cadastra aluno via `multipart/form-data` com campos:
  - `nome` (obrigatório)
  - `whatsapp` (opcional)
  - `turma` (opcional)
  - `foto` (obrigatório)

- `GET /alunos/`  
  Lista alunos cadastrados.

- `POST /chamada/reconhecer`  
  Envia uma imagem (`foto`) e retorna alunos reconhecidos.

---

## Observações / limitações conhecidas

- O “login” no frontend é apenas navegação (não há autenticação real).
- O backend usa CORS liberado (`allow_origins=["*"]`) para facilitar desenvolvimento.
- O arquivo `backend/main.py` tenta servir `../index.html`; no desenvolvimento, recomenda-se rodar **frontend e backend separados** (Vite + Uvicorn).
- `face_recognition` pode ser difícil de instalar em alguns ambientes devido a dependências nativas.

---

## Status do projeto
Este repositório representa a **primeira versão** do sistema e está marcado como **descontinuado**.
