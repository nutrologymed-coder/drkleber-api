from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Optional bearer token protection. If CHATVOLT_TOKEN is set,
# requests must send header: Authorization: Bearer <token>
REQUIRED_TOKEN = os.getenv("CHATVOLT_TOKEN")

# --- Mock database (in-memory for demo) ---
PATIENTS = [
    {"id": "1", "nome": "João Silva", "idade": 45, "diagnostico": "Obesidade Grau I"},
    {"id": "2", "nome": "Maria Santos", "idade": 34, "diagnostico": "Esteatose hepática"},
    {"id": "3", "nome": "Carlos Oliveira", "idade": 52, "diagnostico": "DM2 e sobrepeso"},
]

def _auth_ok():
    if not REQUIRED_TOKEN:
        return True
    auth = request.headers.get("Authorization", "")
    return auth == f"Bearer {REQUIRED_TOKEN}"

@app.before_request
def _check_auth():
    # Protect only API routes (not static or root health check if needed)
    protected_prefixes = ["/pacientes"]
    if any(request.path.startswith(p) for p in protected_prefixes):
        if not _auth_ok():
            return jsonify({"error": "Unauthorized"}), 401

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/pacientes")
def list_pacientes():
    nome = request.args.get("nome", "").strip().lower()
    if nome:
        results = [p for p in PATIENTS if nome in p["nome"].lower()]
    else:
        results = PATIENTS
    return jsonify({"count": len(results), "items": results})

@app.get("/pacientes/<pid>")
def get_paciente(pid):
    for p in PATIENTS:
        if p["id"] == pid:
            return jsonify(p)
    return jsonify({"error": "Paciente não encontrado"}), 404

@app.post("/pacientes")
def create_paciente():
    data = request.get_json(silent=True) or {}
    # Extremely simple validation (demo only)
    required = ["nome", "idade", "diagnostico"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Campos obrigatórios ausentes: {', '.join(missing)}"}), 400
    new_id = str(max(int(p["id"]) for p in PATIENTS) + 1 if PATIENTS else 1)
    data["id"] = new_id
    PATIENTS.append(data)
    return jsonify(data), 201

if __name__ == "__main__":
    # Local dev
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "3000")))
