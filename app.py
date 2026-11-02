from flask import Flask, request, redirect, session, send_from_directory
import json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "los-toxicos-2024-secret"
DATA_FILE = "eventos.json"
DUOS_FILE = "duos.json"
PASSWORD = "toxicos-1.0"
MAX_DUOS = 12

LINK_WHATSAPP = "https://chat.whatsapp.com/KlGw8PxxQYWD0xYLuBlZpk?s=cl&p=a&iam=2"
LINK_FACEBOOK = "https://www.facebook.com/profile.php?id=100024266709108"
LINK_TIKTOK_TOXICOS = "https://www.tiktok.com/@toxicos.de.bermuda"
LINK_TIKTOK_HSR = "https://www.tiktok.com/@hsrramses"
LINK_TIKTOK_BOSTO = "https://www.tiktok.com/@botsto19"
LINK_TIKTOK_RONAN = "https://www.tiktok.com/@ronan7538"

@app.route('/fondo.jpg')
def fondo():
    for n in ["fondo.jpg", "fondo.jpg.jpeg", "fondo.jpeg"]:
        if os.path.exists(n): return send_from_directory(".", n)
    return "", 404

def cargar(): 
    if not os.path.exists(DATA_FILE): return []
    try: 
        with open(DATA_FILE,"r",encoding="utf-8") as f: return json.load(f)
    except: return []

def guardar(d): 
    with open(DATA_FILE,"w",encoding="utf-8") as f: json.dump(d,f,indent=2,ensure_ascii=False)

def cargar_duos():
    if not os.path.exists(DUOS_FILE): return []
    try:
        with open(DUOS_FILE,"r",encoding="utf-8") as f: return json.load(f)
    except: return []

def guardar_duos(d):
    with open(DUOS_FILE,"w",encoding="utf-8") as f: json.dump(d,f,indent=2,ensure_ascii=False)

def es_admin(): return session.get('admin')==True

def estilos():
    return """
    body{background:linear-gradient(rgba(0,0,0,0.7),rgba(10,5,20,0.85)),url('/fondo.jpg');background-size:cover;background-attachment:fixed;background-position:center top;min-height:100vh;margin:0;}
    .card{background:rgba(20,15,35,0.92);backdrop-filter:blur(8px);border:1px solid rgba(168,85,247,0.3);box-shadow:0 0 20px rgba(168,85,247,0.15);border-radius:16px;padding:16px;margin:14px 0;}
    .btn{display:inline-block;padding:12px 22px;border-radius:30px;text-decoration:none;font-weight:bold;margin:6px;color:white;border:none;cursor:pointer}
    .btn-p{background:#a855f7;box-shadow:0 0 15px #a855f780} .wa{background:#25D366} .fb{background:#1877F2} .tt{background:#000;border:1px solid #a855f7} .tt2{background:#1a1a1a;border:1px solid #555}
    input{width:100%;padding:13px;margin:7px 0;border-radius:10px;border:none;box-sizing:border-box}
    """

# ---- HOME ----
@app.route('/')
def home():
    eventos=cargar(); duos=cargar_duos()
    admin_btn = f"<a href='/admin'><button class='btn' style='background:#a855f7'>🔒 Admin</button></a>" if not es_admin() else f"<a href='/logout'><button class='btn' style='background:#ff4444'>Salir</button></a> <a href='/nuevo'><button class='btn btn-p'>+ Evento</button></a> <a href='/registro'><button class='btn' style='background:#333'>Ver Registro</button></a>"

    if not eventos:
        html_e = "<div class='card' style='text-align:center'><div style='font-size:50px'>📭</div><h3 style='color:#a855f7'>No hay eventos aún</h3><p style='opacity:0.8'>Pero síguenos en redes para estar al tiro 🔥</p></div>"
    else:
        html_e="".join([f"<div class='card' style='border-left:4px solid #a855f7'><b>{e['titulo']}</b> - {e['fecha']}<br><small style='opacity:0.7'>{e['lugar']}</small><br><b style='color:#a855f7'>{e.get('marcador','')}</b><br>{e['descripcion']}</div>" for e in eventos])

    # Resumen duos en home
    cupo = f"{len(duos)}/{MAX_DUOS} DÚOS"
    lista_duos_home = "".join([f"<div style='padding:6px 10px;margin:4px 0;background:rgba(255,255,255,0.06);border-radius:8px;font-size:13px'>{i+1}. <b>{d['duo']}</b> | {d['id1']} + {d['id2']} <small style='opacity:0.5'>({d['nombre']})</small></div>" for i,d in enumerate(duos)]) if duos else "<small style='opacity:0.5'>Aún no hay dúos registrados</small>"

    redes = f"""
    <div class='card' style='text-align:center'>
        <h3 style='color:#a855f7;margin:0 0 12px'>🏆 REGISTRO TORNEO 12 DÚOS - {cupo}</h3>
        <a href='/registro' class='btn btn-p' style='font-size:16px;padding:15px 30px'>📝 INSCRIBIR MI DÚO AHORA</a>
        <div style='text-align:left;margin-top:15px;max-height:300px;overflow:auto'>{lista_duos_home}</div>
    </div>

    <div class='card' style='text-align:center'>
        <h3 style='color:#a855f7'>🔥 SÍGUENOS 🔥</h3>
        <a href='{LINK_WHATSAPP}' target='_blank' class='btn wa'>💬 WhatsApp</a>
        <a href='{LINK_FACEBOOK}' target='_blank' class='btn fb'>👥 Facebook</a><br>
        <a href='{LINK_TIKTOK_TOXICOS}' target='_blank' class='btn tt'>☠️ TÓXICOS</a>
        <a href='{LINK_TIKTOK_HSR}' target='_blank' class='btn tt2'>👑 HSRRAMSES</a>
        <a href='{LINK_TIKTOK_BOSTO}' target='_blank' class='btn tt2'>⚔️ BOSTO</a>
        <a href='{LINK_TIKTOK_RONAN}' target='_blank' class='btn tt2'>🔥 RONAN</a>
    </div>
    """
    return f"<meta name='viewport' content='width=device-width, initial-scale=1'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto}} h1{{color:#a855f7;text-align:center;text-shadow:0 0 18px #a855f7;margin:10px 0 0;line-height:1.1}} </style><h1>☠️ TÓXICOS DE<br>BERMUDA ☠️</h1><p style='text-align:center;opacity:0.7;letter-spacing:2px;font-size:13px'>HSR RAMSES EDITION</p><div style='display:flex;justify-content:space-between;align-items:center'><h2>Eventos</h2>{admin_btn}</div>{html_e}{redes}"

# ---- REGISTRO ----
@app.route('/registro', methods=['GET','POST'])
def registro():
    duos=cargar_duos()
    if request.method=='POST':
        if len(duos) >= MAX_DUOS:
            return f"<script>alert('¡Ya se llenaron los {MAX_DUOS} dúos!');window.location='/registro'</script>"
        nuevo = {
            "id": str(int(datetime.now().timestamp())),
            "nombre": request.form['nombre'][:30],
            "duo": request.form['duo'][:30],
            "id1": request.form['id1'][:30],
            "id2": request.form['id2'][:30],
            "fecha": datetime.now().strftime("%d/%m %H:%M")
        }
        # Evitar ID duplicado
        ids_exist = [d['id1'] for d in duos] + [d['id2'] for d in duos]
        if nuevo['id1'] in ids_exist or nuevo['id2'] in ids_exist:
            return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;padding:20px;text-align:center}} </style><div class='card'><h3 style='color:#ff4444'>¡Ese ID ya está registrado!</h3><a href='/registro' class='btn btn-p'>Volver</a></div>"
        duos.append(nuevo)
        guardar_duos(duos)
        return redirect('/registro')

    cupo = len(duos)
    if cupo >= MAX_DUOS:
        form_html = f"<div class='card' style='text-align:center;background:#ff000022;border-color:#ff0000'><h2>🔒 CUPO LLENO</h2><p>Ya se registraron los {MAX_DUOS} dúos. ¡Suerte a todos!</p><a href='/' class='btn btn-p'>Volver al inicio</a></div>"
    else:
        form_html = f"""
        <div class='card'>
            <h3>📝 Registrar mi Dúo ({cupo}/{MAX_DUOS})</h3>
            <p style='opacity:0.7;font-size:13px'>Solo deja tus IDs y entran automático a la lista</p>
            <form method='post'>
                <input name='nombre' placeholder='Tu nombre (ej: Ramses)' required>
                <input name='duo' placeholder='Nombre del Dúo (ej: Los Tóxicos)' required>
                <input name='id1' placeholder='ID Jugador 1 (ej: 12345678)' required>
                <input name='id2' placeholder='ID Jugador 2 (ej: 87654321)' required>
                <button class='btn btn-p' style='width:100%;margin-top:10px'>✅ INSCRIBIRNOS</button>
            </form>
        </div>
        """

    lista = ""
    for i,d in enumerate(duos):
        lista+=f"<div class='card' style='padding:10px 14px;display:flex;justify-content:space-between;align-items:center'><div><b>{i+1}. {d['duo']}</b><br><small>{d['id1']} + {d['id2']} | {d['nombre']} - {d['fecha']}</small></div></div>"
    if not lista: lista="<div class='card' style='text-align:center;opacity:0.6'>Aún no hay dúos. ¡Sé el primero!</div>"

    admin_clear = f"<div style='text-align:center;margin:20px'><a href='/borrar-duos' onclick=\"return confirm('¿Borrar TODOS los dúos?')\" style='color:#ff6666;font-size:12px'>[Admin: Borrar lista]</a></div>" if es_admin() else ""

    return f"<meta name='viewport' content='width=device-width, initial-scale=1'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto}} </style><a href='/' class='btn' style='background:#333'>← Volver</a><h2 style='text-align:center;color:#a855f7'>🏆 TORNEO 12 DÚOS - {cupo}/{MAX_DUOS}</h2>{form_html}<h3 style='margin-top:20px'>Lista de Dúos Registrados</h3>{lista}{admin_clear}"

@app.route('/borrar-duos')
def borrar_duos():
    if not es_admin(): return redirect('/admin')
    guardar_duos([])
    return redirect('/registro')

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method=='POST':
        if request.form.get('password','').strip().lower()==PASSWORD.lower():
            session['admin']=True; return redirect('/')
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;text-align:center;padding:20px}} </style><div class='card'><h2>🔒 Admin</h2><form method='post'><input type='password' name='password' placeholder='Contraseña'><br><button class='btn btn-p'>Entrar</button></form></div>"

@app.route('/logout')
def logout(): session.pop('admin',None); return redirect('/')
@app.route('/nuevo', methods=['GET','POST'])
def nuevo():
    if not es_admin(): return redirect('/admin')
    if request.method=='POST':
        ev=cargar()
        ev.append({"id":str(int(datetime.now().timestamp())),"titulo":request.form['titulo'],"fecha":request.form['fecha'],"lugar":request.form['lugar'],"estado":request.form['estado'],"descripcion":request.form['descripcion'],"marcador":request.form['marcador']})
        guardar(ev); return redirect('/')
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;padding:20px;max-width:600px;margin:auto}} textarea{{width:100%;padding:12px;border-radius:10px;box-sizing:border-box}} </style><div class='card'><h2>Nuevo Evento</h2><form method='post'><input name='titulo' placeholder='Titulo' required><input name='fecha' type='date' required><input name='lugar' placeholder='Lugar' required><select name='estado' style='width:100%;padding:12px;border-radius:10px;margin:8px 0'><option>proximo</option><option>vivo</option><option>finalizado</option></select><textarea name='descripcion' placeholder='Descripcion'></textarea><input name='marcador' placeholder='Marcador'><button class='btn btn-p' style='width:100%;margin-top:10px'>Guardar</button></form></div>"
