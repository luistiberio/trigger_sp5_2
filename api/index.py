from flask import Flask
import requests
import os

app = Flask(__name__)

# Pega o token do ambiente
TOKEN = os.getenv("GH_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Lista de workflows a serem acionados
WORKFLOWS = [
    {"repo": "reporte_hxh_sp5", "workflow": "reporte.yml"},
    {"repo": "backlog", "workflow": "backlog.yml"},
    {"repo": "reportes_sp5", "workflow": "main_script.yml"}, # alterado dados.yml para main_script.yml
    {"repo": "packed_sp5", "workflow": "main_base_to_packed.yaml"},
    {"repo": "queue_list", "workflow": "att10.yml"},
    {"repo": "queue_list", "workflow": "queue_list_sp5.yml"},
    {"repo": "piso_outbound_sp5", "workflow": "piso10.yml"},
    {"repo": "base_packed_go1", "workflow": "main_base_to_packed.yaml"},
    {"repo": "piso_outbound_go2", "workflow": "piso10.yml"},
    {"repo": "reporte_seatalk_go2", "workflow": "piso_go1.yaml"},
]

# Rota principal para verificar se o app está no ar
@app.route('/')
def home():
    return "Servidor do agendador de workflows do GitHub está no ar."

# Rota que será chamada pelo Cron Job da Vercel
@app.route('/api/trigger')
def trigger_workflows():
    # Loop que executa a lógica UMA VEZ por chamada
    for wf in WORKFLOWS:
        url = f"https://api.github.com/repos/luistiberio/{wf['repo']}/actions/workflows/{wf['workflow']}/dispatches"
        data = {"ref": "main"}
        try:
            res = requests.post(url, headers=HEADERS, json=data)
            print(f"[OK] {wf['workflow']} -> {res.status_code}")
        except Exception as e:
            print(f"[ERRO] {wf['workflow']} -> {e}")
    
    return "Workflows acionados com sucesso!", 200
