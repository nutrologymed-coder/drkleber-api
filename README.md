# API de Exemplo (Flask) para Chatvolt

Endpoints:
- `GET /health` → status ok
- `GET /pacientes?nome=<parte-do-nome>` → lista pacientes
- `GET /pacientes/<id>` → paciente por ID
- `POST /pacientes` → cria paciente (JSON: nome, idade, diagnostico)

## Execução local
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PORT=3000
# opcional: export CHATVOLT_TOKEN="seu_token_secreto"
python app.py
```

## Produção no Render
- Conecte o repositório com esses arquivos.
- Tipo: Web Service
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app -b 0.0.0.0:$PORT --preload`
- Variáveis: opcional `CHATVOLT_TOKEN`

## Segurança
Se `CHATVOLT_TOKEN` estiver definido, envie:
```
Authorization: Bearer <seu_token>
```
