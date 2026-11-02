from flask import Flask, request, redirect, session, send_from_directory
import json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "los-toxicos-2024-secret"
DATA_FILE = "eventos.json"
PASSWORD = "toxicos-1.0"

@app.route('/fondo.jpg')
def fondo():
    return send_from_directory(".", "fondo.jpg")

def cargar():
    if not os.path.exists(DATA_FILE): return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return []

def guardar(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def es_admin(): return session.get('admin') == True

def estilos():
    return """
    body{
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.85)), url('/fondo.jpg');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        min-height:100vh;
    }
    """

@app.route('/')
def home():
    eventos = cargar()
    admin_btn = "<a href='/admin'><button>🔒 Admin</button></a>" if not es_admin() else "<a href='/logout'><button style='background:#ff4444'>Salir</button></a> <a href='/nuevo'><button>+ Nuevo</button></a>"
    html=""
    for e in eventos:
        html+=f"<div style='background:rgba(20,15,35,0.88);padding:15px;border-radius:12px;margin:15px 0;border-left:4px solid #a855f7'><b>{e['titulo']}</b> - {e['fecha']}<br>{e['lugar']}<br><b style='color:#a855f7'>{e.get('marcador','')}</b><br>{e['descripcion']}</div>"
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:20px;max-width:600px;margin:auto}} button{{background:#a855f7;color:white;padding:10px 16px;border:none;border-radius:8px;font-weight:bold}} h1{{color:#a855f7;text-align:center;text-shadow:0 0 15px #a855f7}}</style><h1>☠️ TÓXICOS DE BERMUDA ☠️</h1><p style='text-align:center;opacity:0.7'>HSR RAMSES EDITION</p><div style='display:flex;justify-content:space-between'><h2>Eventos</h2>{admin_btn}</div>{html}<div style='text-align:center;margin-top:30px'><a href='https://www.tiktok.com/@toxicos.de.bermuda' style='color:white'>TikTok Oficial</a></div>"

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method=='POST':
        if request.form.get('password','').strip().lower()==PASSWORD.lower():
            session['admin']=True
            return redirect('/')
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;text-align:center;padding:20px}} input{{padding:14px;width:80%;border-radius:8px;border:none;margin:15px}} button{{background:#a855f7;padding:14px 30px;border:none;border-radius:8px;color:white;font-weight:bold}}</style><h2>🔒 Admin</h2><form method='post'><input type='password' name='password'><br><button>Entrar</button></form>"

@app.route('/logout')
def logout():
    session.pop('admin',None)
    return redirect('/')

@app.route('/nuevo', methods=['GET','POST'])
def nuevo():
    if not es_admin(): return redirect('/admin')
    if request.method=='POST':
        ev=cargar()
        ev.append({"id":str(int(datetime.now().timestamp())),"titulo":request.form['titulo'],"fecha":request.form['fecha'],"lugar":request.form['lugar'],"estado":request.form['estado'],"descripcion":request.form['descripcion'],"marcador":request.form['marcador']})
        guardar(ev)
        return redirect('/')
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;padding:20px;max-width:600px;margin:auto}} input,select,textarea{{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:none}} button{{background:#a855f7;padding:12px;width:100%;border:none;border-radius:8px;color:white}}</style><h2>Nuevo</h2><form method='post'><input name='titulo' placeholder='Titulo' required><input name='fecha' type='date' required><input name='lugar' placeholder='Lugar' required><select name='estado'><option>proximo</option><option>vivo</option><option>finalizado</option></select><textarea name='descripcion' placeholder='Descripcion'></textarea><input name='marcador' placeholder='Marcador'><button>Guardar</button></form>"
