from flask import Flask, request, redirect, session, send_from_directory
import json, os, re
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "los-toxicos-2024-secret"
DATA_FILE = "eventos.json"
DUOS_FILE = "duos.json"
VIDEOS_FILE = "videos.json"
UPLOAD_FOLDER = "uploads/videos"
PASSWORD = "toxicos-1.0"
MAX_DUOS = 12
ALLOWED_EXT = {'mp4','mov','webm','mkv'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

@app.route('/uploads/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

def cargar(): 
    if not os.path.exists(DATA_FILE): return []
    try: return json.load(open(DATA_FILE,"r",encoding="utf-8"))
    except: return []
def guardar(d): json.dump(d, open(DATA_FILE,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
def cargar_duos():
    if not os.path.exists(DUOS_FILE): return []
    try: return json.load(open(DUOS_FILE,"r",encoding="utf-8"))
    except: return []
def guardar_duos(d): json.dump(d, open(DUOS_FILE,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
def cargar_videos():
    if not os.path.exists(VIDEOS_FILE): return []
    try: return json.load(open(VIDEOS_FILE,"r",encoding="utf-8"))
    except: return []
def guardar_videos(d): json.dump(d, open(VIDEOS_FILE,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
def es_admin(): return session.get('admin')==True

def get_youtube_id(url):
    if not url: return None
    m = re.search(r'(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{6,})', url)
    return m.group(1) if m else None

def estilos():
    return """
    body{background:linear-gradient(rgba(0,0,0,0.7),rgba(10,5,20,0.85)),url('/fondo.jpg');background-size:cover;background-attachment:fixed;background-position:center top;min-height:100vh;margin:0;}
    .card{background:rgba(20,15,35,0.92);backdrop-filter:blur(8px);border:1px solid rgba(168,85,247,0.3);box-shadow:0 0 20px rgba(168,85,247,0.15);border-radius:16px;padding:16px;margin:14px 0;}
    .btn{display:inline-block;padding:12px 22px;border-radius:30px;text-decoration:none;font-weight:bold;margin:6px;color:white;border:none;cursor:pointer;text-align:center}
    .btn-p{background:#a855f7;box-shadow:0 0 15px #a855f780} .wa{background:#25D366} .fb{background:#1877F2} .tt{background:#000;border:1px solid #a855f7} .tt2{background:#1a1a1a;border:1px solid #555}
    input,textarea,select{width:100%;padding:13px;margin:7px 0;border-radius:10px;border:none;box-sizing:border-box}
    video,iframe{width:100%;border-radius:12px;background:#000;border:none}
    .tabs{display:flex;gap:8px;margin:10px 0}
    .tab{flex:1;padding:10px;border-radius:10px;text-align:center;cursor:pointer;background:#222;color:white;border:1px solid #444}
    .tab.active{background:#a855f7;border-color:#a855f7}
    """

@app.route('/')
def home():
    eventos=cargar(); duos=cargar_duos(); videos=cargar_videos()[:3]
    admin_btn = f"<a href='/admin'><button class='btn' style='background:#a855f7'>🔒 Admin</button></a>" if not es_admin() else f"<a href='/logout'><button class='btn' style='background:#ff4444'>Salir</button></a> <a href='/nuevo'><button class='btn btn-p'>+ Evento</button></a>"
    html_e = "<div class='card' style='text-align:center'><div style='font-size:50px'>📭</div><h3 style='color:#a855f7'>No hay eventos aún</h3></div>" if not eventos else "".join([f"<div class='card' style='border-left:4px solid #a855f7'><b>{e['titulo']}</b> - {e['fecha']}<br><small>{e['lugar']}</small><br><b style='color:#a855f7'>{e.get('marcador','')}</b><br>{e['descripcion']}</div>" for e in eventos])
    cupo = f"{len(duos)}/{MAX_DUOS} DÚOS"
    lista_home = "".join([f"<div style='padding:6px 10px;margin:4px 0;background:rgba(255,255,255,0.06);border-radius:8px;font-size:13px'>{i+1}. <b>{d['duo']}</b> | {d['id1']} + {d['id2']}</div>" for i,d in enumerate(duos)]) if duos else "<small style='opacity:0.5'>Aún no hay dúos</small>"
    videos_home = ""
    if videos:
        videos_home = "<h3 style='color:#a855f7'>🎬 ÚLTIMOS CLIPS</h3>"
        for v in reversed(videos[-3:]):
            yt = get_youtube_id(v.get('link',''))
            if yt:
                videos_home+=f"<div class='card'><iframe height='220' src='https://www.youtube.com/embed/{yt}' allowfullscreen></iframe><b>{v['titulo']}</b></div>"
            elif v.get('file'):
                videos_home+=f"<div class='card'><video controls><source src='/uploads/videos/{v['file']}'></video><b>{v['titulo']}</b></div>"
            else:
                videos_home+=f"<div class='card'><b>{v['titulo']}</b><br><a href='{v.get('link')}' target='_blank' class='btn tt' style='width:90%'>Ver en TikTok / YouTube</a></div>"
    redes = f"""
    <div class='card' style='text-align:center'>
        <h3 style='color:#a855f7'>🏆 TORNEO {cupo}</h3>
        <a href='/registro' class='btn btn-p'>📝 INSCRIBIR DÚO</a>
        <a href='/videos' class='btn' style='background:#333'>🎬 VER CLIPS</a>
        <div style='text-align:left;margin-top:15px;max-height:200px;overflow:auto'>{lista_home}</div>
    </div>{videos_home}
    <div class='card' style='text-align:center'>
        <h3 style='color:#a855f7'>🔥 SÍGUENOS 🔥</h3>
        <a href='{LINK_WHATSAPP}' target='_blank' class='btn wa'>💬 WhatsApp</a>
        <a href='{LINK_FACEBOOK}' target='_blank' class='btn fb'>👥 Facebook</a><br>
        <a href='{LINK_TIKTOK_TOXICOS}' target='_blank' class='btn tt'>☠️ TÓXICOS</a>
        <a href='{LINK_TIKTOK_HSR}' target='_blank' class='btn tt2'>👑 HSRRAMSES</a>
        <a href='{LINK_TIKTOK_BOSTO}' target='_blank' class='btn tt2'>⚔️ BOSTO</a>
        <a href='{LINK_TIKTOK_RONAN}' target='_blank' class='btn tt2'>🔥 RONAN</a>
    </div>"""
    return f"<meta name='viewport' content='width=device-width, initial-scale=1'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto}} h1{{color:#a855f7;text-align:center;text-shadow:0 0 18px #a855f7;margin:10px 0 0}} </style><h1>☠️ TÓXICOS DE<br>BERMUDA ☠️</h1><p style='text-align:center;opacity:0.7;letter-spacing:2px;font-size:13px'>HSR RAMSES EDITION</p><div style='display:flex;justify-content:space-between'><h2>Eventos</h2>{admin_btn}</div>{html_e}{redes}"

@app.route('/videos')
def pag_videos():
    videos=cargar_videos()
    admin_add = f"<a href='/subir-video'><button class='btn btn-p'>+ Subir Video</button></a>" if es_admin() else ""
    html=""
    if not videos:
        html="<div class='card' style='text-align:center'><h3>🎬 No hay clips aún</h3></div>"
    else:
        for v in reversed(videos):
            del_btn = f"<div style='text-align:right'><a href='/borrar-video/{v['id']}' onclick=\"return confirm('¿Borrar?')\" style='color:#ff6666;font-size:12px'>Borrar</a></div>" if es_admin() else ""
            yt = get_youtube_id(v.get('link',''))
            if yt:
                html+=f"<div class='card'><iframe height='280' src='https://www.youtube.com/embed/{yt}' allowfullscreen></iframe><div style='margin-top:10px'><b>{v['titulo']}</b> <span style='background:#a855f7;padding:3px 8px;border-radius:20px;font-size:10px'>{v['tipo'].upper()}</span><br><small style='opacity:0.6'>{v['descripcion']}</small></div>{del_btn}</div>"
            elif v.get('file'):
                html+=f"<div class='card'><video controls playsinline><source src='/uploads/videos/{v['file']}'></video><div style='margin-top:10px'><b>{v['titulo']}</b> <span style='background:#25D366;padding:3px 8px;border-radius:20px;font-size:10px'>{v['tipo'].upper()}</span><br><small style='opacity:0.6'>{v['descripcion']}</small></div>{del_btn}</div>"
            else:
                html+=f"<div class='card'><div style='text-align:center;padding:20px'><b>{v['titulo']}</b><br><small style='opacity:0.6'>{v['descripcion']}</small><br><a href='{v.get('link')}' target='_blank' class='btn btn-p' style='margin-top:10px'>▶️ VER EN TIKTOK / YOUTUBE</a></div>{del_btn}</div>"
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto}} </style><a href='/' class='btn' style='background:#333'>← Inicio</a><div style='display:flex;justify-content:space-between;align-items:center'><h2>🎬 Clips y Tutoriales</h2>{admin_add}</div>{html}"

@app.route('/subir-video', methods=['GET','POST'])
def subir_video():
    if not es_admin(): return redirect('/admin')
    if request.method=='POST':
        titulo=request.form['titulo'][:60]
        descripcion=request.form['descripcion'][:200]
        tipo=request.form['tipo']
        link=request.form.get('link','').strip()
        filename=None
        file = request.files.get('video')
        if file and file.filename!='':
            ext=file.filename.rsplit('.',1)[-1].lower()
            if ext in ALLOWED_EXT:
                filename=f"{int(datetime.now().timestamp())}_{secure_filename(file.filename)}"
                file.save(os.path.join(UPLOAD_FOLDER, filename))
        if not filename and not link:
            return "Tienes que subir archivo O pegar link"
        videos=cargar_videos()
        videos.append({"id":str(int(datetime.now().timestamp())),"titulo":titulo,"descripcion":descripcion,"tipo":tipo,"file":filename,"link":link,"fecha":datetime.now().strftime("%d/%m/%Y")})
        guardar_videos(videos)
        return redirect('/videos')
    return f"""
    <meta name='viewport' content='width=device-width'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto}} </style>
    <a href='/videos' class='btn' style='background:#333'>← Volver</a>
    <div class='card'><h2>📤 Subir Clip / Tutorial</h2>
    <form method='post' enctype='multipart/form-data'>
        <input name='titulo' placeholder='Título (ej: Cómo hacer 1vs4 en Bermuda)' required>
        <select name='tipo'><option value='clip'>🎮 Clip / Jugada</option><option value='tutorial'>📚 Tutorial</option></select>
        <textarea name='descripcion' placeholder='Descripción corta' rows='2'></textarea>
        <div style='background:rgba(168,85,247,0.15);padding:12px;border-radius:10px;margin:10px 0'>
            <b>OPCIÓN 1: Subir archivo</b><br><small style='opacity:0.7'>MP4, MOV, WEBM (max 100MB) - Se borra si reinstalas Render</small>
            <input type='file' name='video' accept='video/*' style='background:white;color:black'>
        </div>
        <div style='background:rgba(37,211,102,0.15);padding:12px;border-radius:10px;margin:10px 0'>
            <b>OPCIÓN 2: Pegar link (RECOMENDADO)</b><br><small style='opacity:0.7'>Pega link de YouTube, TikTok o Shorts - Nunca se borra</small>
            <input name='link' placeholder='https://youtube.com/watch?v=... o https://tiktok.com/...'>
        </div>
        <button class='btn btn-p' style='width:100%;margin-top:12px'>✅ PUBLICAR</button>
    </form>
    <p style='font-size:12px;opacity:0.5;text-align:center'>Puedes usar una opción o las dos. Si pones link de YouTube se ve directo en la página.</p>
    </div>
    """

@app.route('/borrar-video/<id>')
def borrar_video(id):
    if not es_admin(): return redirect('/admin')
    videos=cargar_videos()
    for v in videos:
        if v['id']==id and v.get('file'):
            try: os.remove(os.path.join(UPLOAD_FOLDER, v['file']))
            except: pass
    guardar_videos([v for v in videos if v['id']!=id])
    return redirect('/videos')

@app.route('/registro', methods=['GET','POST'])
def registro():
    duos=cargar_duos()
    if request.method=='POST':
        if len(duos)>=MAX_DUOS: return "<script>alert('Cupo lleno');location='/registro'</script>"
        nuevo={"id":str(int(datetime.now().timestamp())),"nombre":request.form['nombre'][:30],"duo":request.form['duo'][:30],"id1":request.form['id1'][:30],"id2":request.form['id2'][:30],"fecha":datetime.now().strftime("%d/%m %H:%M")}
        ids_exist=[d['id1'] for d in duos]+[d['id2'] for d in duos]
        if nuevo['id1'] in ids_exist or nuevo['id2'] in ids_exist:
            return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;padding:20px;text-align:center}} </style><div class='card'><h3 style='color:#ff4444'>¡Ese ID ya está registrado!</h3><a href='/registro' class='btn btn-p'>Volver</a></div>"
        duos.append(nuevo); guardar_duos(duos); return redirect('/registro')
    cupo=len(duos)
    form_html=f"<div class='card' style='text-align:center;background:#ff000022'><h2>🔒 CUPO LLENO</h2></div>" if cupo>=MAX_DUOS else f"<div class='card'><h3>📝 Registrar mi Dúo ({cupo}/{MAX_DUOS})</h3><form method='post'><input name='nombre' placeholder='Tu nombre' required><input name='duo' placeholder='Nombre del Dúo' required><input name='id1' placeholder='ID Jugador 1' required><input name='id2' placeholder='ID Jugador 2' required><button class='btn btn-p' style='width:100%;margin-top:10px'>✅ INSCRIBIRNOS</button></form></div>"
    lista="".join([f"<div class='card' style='padding:10px 14px'><b>{i+1}. {d['duo']}</b><br><small>{d['id1']} + {d['id2']} | {d['nombre']}</small></div>" for i,d in enumerate(duos)]) or "<div class='card' style='text-align:center;opacity:0.6'>Aún no hay dúos</div>"
    admin_clear=f"<div style='text-align:center'><a href='/borrar-duos' onclick=\"return confirm('¿Borrar TODOS?')\" style='color:#ff6666;font-size:12px'>[Admin: Borrar lista]</a></div>" if es_admin() else ""
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto}} </style><a href='/' class='btn' style='background:#333'>← Volver</a><h2 style='text-align:center;color:#a855f7'>🏆 TORNEO 12 DÚOS - {cupo}/{MAX_DUOS}</h2>{form_html}{lista}{admin_clear}"

@app.route('/borrar-duos')
def borrar_duos():
    if not es_admin(): return redirect('/admin')
    guardar_duos([]); return redirect('/registro')

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
        ev=cargar(); ev.append({"id":str(int(datetime.now().timestamp())),"titulo":request.form['titulo'],"fecha":request.form['fecha'],"lugar":request.form['lugar'],"estado":request.form['estado'],"descripcion":request.form['descripcion'],"marcador":request.form['marcador']}); guardar(ev); return redirect('/')
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;padding:20px;max-width:600px;margin:auto}} textarea{{width:100%;padding:12px;border-radius:10px;box-sizing:border-box}} </style><div class='card'><h2>Nuevo Evento</h2><form method='post'><input name='titulo' placeholder='Titulo' required><input name='fecha' type='date' required><input name='lugar' placeholder='Lugar' required><select name='estado' style='width:100%;padding:12px;border-radius:10px;margin:8px 0'><option>proximo</option><option>vivo</option><option>finalizado</option></select><textarea name='descripcion' placeholder='Descripcion'></textarea><input name='marcador' placeholder='Marcador'><button class='btn btn-p' style='width:100%;margin-top:10px'>Guardar</button></form></div>"
