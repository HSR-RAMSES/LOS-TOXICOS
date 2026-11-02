from flask import Flask, request, redirect, session, send_from_directory
import json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "los-toxicos-2024-secret"
DATA_FILE = "eventos.json"
PASSWORD = "toxicos-1.0"

LINK_WHATSAPP = "https://chat.whatsapp.com/KlGw8PxxQYWD0xYLuBlZpk?s=cl&p=a&iam=2"
LINK_FACEBOOK = "https://www.facebook.com/profile.php?id=100024266709108"
LINK_TIKTOK_TOXICOS = "https://www.tiktok.com/@toxicos.de.bermuda?_r=1&_t=ZS-9B3UA4rcikW"
LINK_TIKTOK_HSR = "https://www.tiktok.com/@hsrramses"
LINK_TIKTOK_BOSTO = "https://www.tiktok.com/@botsto19?_r=1&_t=ZS-9B3UDEGRl6z"
LINK_TIKTOK_RONAN = "https://www.tiktok.com/@ronan7538?_r=1&_t=ZS-9B3U8Gggjjg"

@app.route('/fondo.jpg')
def fondo():
    for nombre in ["fondo.jpg", "fondo.jpg.jpeg", "fondo.jpeg"]:
        if os.path.exists(nombre):
            return send_from_directory(".", nombre)
    return "No fondo", 404

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
        background: linear-gradient(rgba(0,0,0,0.7), rgba(10,5,20,0.85)), url('/fondo.jpg');
        background-size: cover;
        background-attachment: fixed;
        background-position: center top;
        min-height:100vh;
        margin:0;
    }
    .card-evento{
        background: rgba(20, 15, 35, 0.92);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(168, 85, 247, 0.3);
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.15);
    }
    .btn-social{
        display:inline-block;
        padding:12px 20px;
        border-radius:30px;
        text-decoration:none;
        font-weight:bold;
        margin:6px;
        color:white;
        font-size:14px;
    }
    .wa{ background:#25D366; }
    .fb{ background:#1877F2; }
    .tt{ background:#000; border:1px solid #a855f7; }
    .tt2{ background:#1a1a1a; border:1px solid #555; }
    """

@app.route('/')
def home():
    eventos = cargar()
    admin_btn = f"<a href='/admin'><button style='background:#a855f7;color:white;padding:10px 18px;border:none;border-radius:20px;font-weight:bold'>🔒 Admin</button></a>" if not es_admin() else f"<a href='/logout'><button style='background:#ff4444;color:white;padding:8px 14px;border:none;border-radius:20px'>Salir</button></a> <a href='/nuevo'><button style='background:#a855f7;color:white;padding:8px 14px;border:none;border-radius:20px'>+ Nuevo</button></a>"
    
    if not eventos:
        html_eventos = """
        <div class='card-evento' style='padding:30px 20px;border-radius:16px;text-align:center;margin:20px 0;'>
            <div style='font-size:50px'>📭</div>
            <h3 style='margin:10px 0;color:#a855f7'>No hay eventos aún</h3>
            <p style='opacity:0.85;line-height:1.6'>Pero no te pierdas nada, síguenos en nuestras redes sociales para estar al tiro de los próximos partidos 🔥<br>¡Puro Tóxico de Bermuda!</p>
        </div>
        """
    else:
        html_eventos = ""
        for e in eventos:
            html_eventos+=f"<div class='card-evento' style='padding:15px;border-radius:12px;margin:15px 0;border-left:4px solid #a855f7'><b style='font-size:16px'>{e['titulo']}</b> - {e['fecha']}<br><small style='opacity:0.7'>{e['lugar']}</small><br><b style='color:#a855f7'>{e.get('marcador','')}</b><br><span style='opacity:0.9'>{e['descripcion']}</span></div>"

    redes = f"""
    <div style='text-align:center;margin-top:25px;padding:22px;background:rgba(0,0,0,0.55);border-radius:20px;border:1px solid rgba(168,85,247,0.2)'>
        <h3 style='color:#a855f7;margin:0 0 15px 0;'>🔥 SÍGUENOS 🔥</h3>
        <div style='margin-bottom:12px'>
            <a href='{LINK_WHATSAPP}' target='_blank' class='btn-social wa'>💬 WhatsApp TÓXICOS</a>
            <a href='{LINK_FACEBOOK}' target='_blank' class='btn-social fb'>👥 Facebook</a>
        </div>
        <div style='border-top:1px solid rgba(255,255,255,0.1);margin:15px 0;padding-top:15px'>
            <p style='font-size:13px;opacity:0.6;margin:0 0 10px 0;letter-spacing:1px'>TIKTOKS OFICIALES</p>
            <a href='{LINK_TIKTOK_TOXICOS}' target='_blank' class='btn-social tt'>☠️ TÓXICOS DE BERMUDA</a><br>
            <a href='{LINK_TIKTOK_HSR}' target='_blank' class='btn-social tt2'>👑 HSRRAMSES</a>
            <a href='{LINK_TIKTOK_BOSTO}' target='_blank' class='btn-social tt2'>⚔️ BOSTO</a>
            <a href='{LINK_TIKTOK_RONAN}' target='_blank' class='btn-social tt2'>🔥 RONAN</a>
        </div>
        <p style='font-size:11px;opacity:0.4;margin-top:18px'>HSR RAMSES EDITION</p>
    </div>
    """
    return f"<meta name='viewport' content='width=device-width, initial-scale=1'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:620px;margin:auto}} h1{{color:#a855f7;text-align:center;text-shadow:0 0 18px #a855f7;margin:10px 0 0 0;line-height:1.1}} </style><h1>☠️ TÓXICOS DE<br>BERMUDA ☠️</h1><p style='text-align:center;opacity:0.7;letter-spacing:2px;font-size:13px;margin-top:5px'>HSR RAMSES EDITION</p><div style='display:flex;justify-content:space-between;align-items:center;margin:20px 0 10px 0'><h2 style='margin:0'>Eventos</h2>{admin_btn}</div>{html_eventos}{redes}"

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method=='POST':
        if request.form.get('password','').strip().lower()==PASSWORD.lower():
            session['admin']=True
            return redirect('/')
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;text-align:center;padding:20px}} input{{padding:14px;width:80%;border-radius:10px;border:none;margin:15px}} button{{background:#a855f7;padding:14px 30px;border:none;border-radius:10px;color:white;font-weight:bold}}</style><h2>🔒 Admin</h2><form method='post'><input type='password' name='password' placeholder='Contraseña'><br><button>Entrar</button></form>"

@app.route('/logout')
def logout():
    session.pop('admin',None)
    return redirect('/')

@app.route('/nuevo', methods=['GET','POST'])
def nuevo():
    if not es_admin(): return redirect('/admin')
    if request.method=='POST':
        ev=cargar()
        nuevo_evento = {
            "id": str(int(datetime.now().timestamp())),
            "titulo": request.form['titulo'],
            "fecha": request.form['fecha'],
            "lugar": request.form['lugar'],
            "estado": request.form['estado'],
            "descripcion": request.form['descripcion'],
            "marcador": request.form['marcador']
        }
        ev.append(nuevo_evento)
        guardar(ev)
        return redirect('/')
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;padding:20px;max-width:600px;margin:auto}} input,select,textarea{{width:100%;padding:12px;margin:8px 0;border-radius:10px;border:none;box-sizing:border-box}} button{{background:#a855f7;padding:12px;width:100%;border:none;border-radius:10px;color:white;font-weight:bold}}</style><h2>Nuevo Evento</h2><form method='post'><input name='titulo' placeholder='Titulo' required><input name='fecha' type='date' required><input name='lugar' placeholder='Lugar' required><select name='estado'><option>proximo</option><option>vivo</option><option>finalizado</option></select><textarea name='descripcion' placeholder='Descripcion'></textarea><input name='marcador' placeholder='Marcador'><button>Guardar</button></form>"
