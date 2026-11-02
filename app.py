from flask import Flask, request, redirect, session, send_from_directory, jsonify
import json, os, re
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "los-toxicos-2024-secret"
DATA_FILE = "eventos.json"
DUOS_FILE = "duos.json"
VIDEOS_FILE = "videos.json"
CHATS_FILE = "chats.json"
UPLOAD_FOLDER = "uploads/videos"
PASSWORD = "toxicos-1.0"
MAX_DUOS = 12
ALLOWED_EXT = {'mp4','mov','webm','mkv'}

# ====== VIDEOS Y EVENTOS QUE NUNCA SE BORRAN ======
VIDEOS_FIJOS = [
    {
        "id": "clip-pases-fijo",
        "titulo": "ENTREGANDO PASES A LOS INTEGRANTES DE LA COMUNIDAD",
        "descripcion": "HSR Ramses entregando pases - Tóxicos de Bermuda",
        "tipo": "clip",
        "file": None,
        "link": "https://vt.tiktok.com/ZSgEp7nde/",
        "fecha": "02/11/2025"
    }
]
EVENTOS_FIJOS = []
# =================================================

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
    if not os.path.exists(DATA_FILE): return EVENTOS_FIJOS
    try: 
        datos = json.load(open(DATA_FILE,"r",encoding="utf-8"))
        return datos if datos else EVENTOS_FIJOS
    except: return EVENTOS_FIJOS
def guardar(d): json.dump(d, open(DATA_FILE,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
def cargar_duos():
    if not os.path.exists(DUOS_FILE): return []
    try: return json.load(open(DUOS_FILE,"r",encoding="utf-8"))
    except: return []
def guardar_duos(d): json.dump(d, open(DUOS_FILE,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
def cargar_videos():
    fijos = VIDEOS_FIJOS
    if not os.path.exists(VIDEOS_FILE): return fijos
    try: 
        din = json.load(open(VIDEOS_FILE,"r",encoding="utf-8"))
        return fijos + din
    except: return fijos
def guardar_videos(d): 
    solo_dinamicos = [v for v in d if v.get('id','') not in [x['id'] for x in VIDEOS_FIJOS]]
    json.dump(solo_dinamicos, open(VIDEOS_FILE,"w",encoding="utf-8"), indent=2, ensure_ascii=False)

def cargar_chats():
    if not os.path.exists(CHATS_FILE): return []
    try: return json.load(open(CHATS_FILE,"r",encoding="utf-8"))
    except: return []
def guardar_chats(d): json.dump(d, open(CHATS_FILE,"w",encoding="utf-8"), indent=2, ensure_ascii=False)

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
    """

def widget_bot():
    return """
    <div id='bot-hsr-btn' style='position:fixed;bottom:20px;right:20px;z-index:9999;background:#a855f7;color:white;padding:14px 22px;border-radius:30px;font-weight:bold;box-shadow:0 0 20px #a855f7aa;cursor:pointer;' onclick='toggleBot()'>🤖 BOT-HSR</div>
    <div id='bot-hsr-chat' style='display:none;position:fixed;bottom:85px;right:15px;z-index:9999;width:340px;max-width:90vw;height:420px;background:#141023;border:1px solid #a855f7;border-radius:16px;overflow:hidden;flex-direction:column'>
        <div style='background:#a855f7;padding:12px 15px;display:flex;justify-content:space-between;color:white'><b>🤖 BOT-HSR - HSR Ramses</b><span onclick='toggleBot()' style='cursor:pointer'>✕</span></div>
        <div id='bot-messages' style='flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px;background:#0a0614'></div>
        <div style='padding:10px;background:#141023'><input id='bot-name' placeholder='Tu nombre' style='padding:10px;border-radius:8px;border:none;width:100%;margin-bottom:6px'><div style='display:flex;gap:6px'><input id='bot-input' placeholder='Escribe tu duda...' style='flex:1;padding:10px;border-radius:8px;border:none'><button onclick='sendBot()' style='background:#a855f7;border:none;color:white;padding:10px 14px;border-radius:8px;font-weight:bold'>➤</button></div></div>
    </div>
    <script>
    let chatId = localStorage.getItem('hsr_chat_id') || null; let open = false;
    function toggleBot(){ open = !open; document.getElementById('bot-hsr-chat').style.display = open ? 'flex' : 'none'; if(open) loadBot(); }
    function addMsg(t,f){ const d=document.createElement('div'); d.style.cssText=f=='user'?'align-self:flex-end;background:#a855f7;color:white;padding:8px 12px;border-radius:14px 14px 0 14px;max-width:80%;font-size:13px':'align-self:flex-start;background:#222;color:white;padding:8px 12px;border-radius:14px 14px 14px 0;max-width:80%;font-size:13px'; d.innerText=t; document.getElementById('bot-messages').appendChild(d); document.getElementById('bot-messages').scrollTop=99999; }
    async function loadBot(){ if(!chatId) return; const r=await fetch('/chat/get?chat_id='+chatId); const data=await r.json(); document.getElementById('bot-messages').innerHTML=''; data.messages.forEach(m=>addMsg(m.text,m.from)); }
    async function sendBot(){ const name=document.getElementById('bot-name').value||'Anon'; const text=document.getElementById('bot-input').value; if(!text.trim()) return; addMsg(text,'user'); document.getElementById('bot-input').value=''; const r=await fetch('/chat/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chat_id:chatId,name:name,text:text})}); const d=await r.json(); chatId=d.chat_id; localStorage.setItem('hsr_chat_id',chatId); localStorage.setItem('hsr_chat_name',name); setTimeout(loadBot,500); }
    document.getElementById('bot-input').addEventListener('keydown',e=>{if(e.key==='Enter') sendBot();});
    document.getElementById('bot-name').value = localStorage.getItem('hsr_chat_name') || '';
    setInterval(()=>{if(open&&chatId) loadBot();},3000);
    </script>
    """

@app.route('/')
def home():
    eventos=cargar(); duos=cargar_duos(); videos=cargar_videos()[:3]
    admin_btn = f"<a href='/admin'><button class='btn' style='background:#a855f7'>🔒 Admin</button></a>" if not es_admin() else f"<a href='/mensajes'><button class='btn' style='background:#ffaa00'>💬 Mensajes ({len(cargar_chats())})</button></a> <a href='/logout'><button class='btn' style='background:#ff4444'>Salir</button></a> <a href='/nuevo'><button class='btn btn-p'>+ Evento</button></a>"
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
                link = v.get('link','')
                if link:
                    videos_home+=f"<div class='card' style='padding:0;overflow:hidden'><div style='padding:12px'><b>{v['titulo']}</b><br><small style='opacity:0.6'>{v['descripcion']}</small></div><a href='{link}' target='_blank' style='display:block;background:#000;text-align:center;padding:12px;color:white;text-decoration:none;font-weight:bold'>▶️ VER EN TIKTOK</a></div>"
    redes = f"""
    <div class='card' style='text-align:center'>
        <h3 style='color:#a855f7;margin:0 0 12px'>🏆 TORNEO {cupo}</h3>
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
    return f"<meta name='viewport' content='width=device-width, initial-scale=1'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto;padding-bottom:90px}} h1{{color:#a855f7;text-align:center;text-shadow:0 0 18px #a855f7;margin:10px 0 0}} </style><h1>☠️ TÓXICOS DE<br>BERMUDA ☠️</h1><p style='text-align:center;opacity:0.7;letter-spacing:2px;font-size:13px'>HSR RAMSES EDITION</p><div style='display:flex;justify-content:space-between'><h2>Eventos</h2>{admin_btn}</div>{html_e}{redes}{widget_bot()}"

@app.route('/chat/send', methods=['POST'])
def chat_send():
    data = request.get_json(); chat_id = data.get('chat_id'); text = data.get('text','').strip()[:500]; name = data.get('name','Anon')[:30]
    if not text: return jsonify({"error":"vacio"})
    chats = cargar_chats()
    if not chat_id:
        chat_id = str(int(datetime.now().timestamp()*1000))
        chats.append({"id":chat_id,"name":name,"last":datetime.now().strftime("%d/%m %H:%M"),"messages":[{"from":"user","text":text,"time":datetime.now().strftime("%H:%M")}]})
    else:
        for c in chats:
            if c['id']==chat_id: c['last']=datetime.now().strftime("%d/%m %H:%M"); c['name']=name; c['messages'].append({"from":"user","text":text,"time":datetime.now().strftime("%H:%M")}); break
        else: chats.append({"id":chat_id,"name":name,"last":datetime.now().strftime("%d/%m %H:%M"),"messages":[{"from":"user","text":text,"time":datetime.now().strftime("%H:%M")}]})
    guardar_chats(chats); return jsonify({"chat_id":chat_id})

@app.route('/chat/get')
def chat_get():
    chat_id = request.args.get('chat_id'); chats = cargar_chats()
    for c in chats:
        if c['id']==chat_id: return jsonify(c)
    return jsonify({"messages":[]})

@app.route('/chat/admin_send', methods=['POST'])
def chat_admin_send():
    if not es_admin(): return jsonify({"error":"no admin"})
    data = request.get_json(); chat_id = data.get('chat_id'); text = data.get('text','').strip()[:500]
    chats = cargar_chats()
    for c in chats:
        if c['id']==chat_id: c['messages'].append({"from":"admin","text":text,"time":datetime.now().strftime("%H:%M")})
    guardar_chats(chats); return jsonify({"ok":True})

@app.route('/mensajes')
def mensajes():
    if not es_admin(): return redirect('/admin')
    chats = cargar_chats()
    html_chats = "".join([f"<div class='card' style='cursor:pointer' onclick=\"openChat('{c['id']}','{c['name']}')\"><b>{c['name']}</b> <small style='opacity:0.5'>{c['last']}</small><br><small>{c['messages'][-1]['text'][:40]}...</small></div>" for c in chats]) or "<div class='card'>No hay mensajes aún</div>"
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto;padding-bottom:90px}} </style><a href='/' class='btn' style='background:#333'>← Inicio</a><h2>💬 Mensajes BOT-HSR</h2><div style='display:flex;gap:10px;flex-wrap:wrap'><div style='flex:1;min-width:280px'>{html_chats}</div><div id='chat-view' style='flex:1.5;display:none;min-width:280px' class='card'><div id='chat-view-name' style='font-weight:bold;color:#a855f7'></div><div id='chat-view-msgs' style='height:300px;overflow:auto;display:flex;flex-direction:column;gap:6px;background:#0a0614;padding:10px;border-radius:10px'></div><div style='display:flex;gap:6px;margin-top:10px'><input id='admin-input' placeholder='Responde como HSR Ramses...'><button onclick='sendAdmin()' class='btn btn-p'>Enviar</button></div><a id='del-chat' href='#' style='color:#ff6666;font-size:12px'>Borrar</a></div></div><script>let curId=null;function openChat(id,name){{curId=id;document.getElementById('chat-view').style.display='block';document.getElementById('chat-view-name').innerText=name;document.getElementById('del-chat').href='/borrar-chat/'+id;loadAdminChat();}}async function loadAdminChat(){{if(!curId) return;const r=await fetch('/chat/get?chat_id='+curId);const data=await r.json();const cont=document.getElementById('chat-view-msgs');cont.innerHTML='';data.messages.forEach(m=>{{const d=document.createElement('div');d.style.cssText=m.from=='user'?'align-self:flex-start;background:#222;padding:8px 12px;border-radius:12px;max-width:80%;font-size:13px':'align-self:flex-end;background:#a855f7;padding:8px 12px;border-radius:12px;max-width:80%';d.innerText=m.text;cont.appendChild(d);}});cont.scrollTop=9999;}}async function sendAdmin(){{const t=document.getElementById('admin-input').value;if(!t.trim()) return;await fetch('/chat/admin_send',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{chat_id:curId,text:t}})}});document.getElementById('admin-input').value='';loadAdminChat();}}setInterval(()=>{{if(curId) loadAdminChat();}},2000);</script>{widget_bot()}"

@app.route('/borrar-chat/<id>')
def borrar_chat(id):
    if not es_admin(): return redirect('/admin')
    guardar_chats([c for c in cargar_chats() if c['id']!=id]); return redirect('/mensajes')

@app.route('/videos')
def pag_videos():
    videos=cargar_videos()
    admin_add = f"<a href='/subir-video'><button class='btn btn-p'>+ Subir Video</button></a>" if es_admin() else ""
    html=""
    if not videos:
        html="<div class='card' style='text-align:center'><h3>🎬 No hay clips aún</h3></div>"
    else:
        for v in reversed(videos):
            yt = get_youtube_id(v.get('link',''))
            if yt:
                html+=f"<div class='card'><iframe height='280' src='https://www.youtube.com/embed/{yt}' allowfullscreen></iframe><div style='margin-top:10px'><b>{v['titulo']}</b><br><small style='opacity:0.6'>{v['descripcion']}</small></div></div>"
            elif v.get('file'):
                html+=f"<div class='card'><video controls playsinline><source src='/uploads/videos/{v['file']}'></video><div style='margin-top:10px'><b>{v['titulo']}</b><br><small style='opacity:0.6'>{v['descripcion']}</small></div></div>"
            else:
                html+=f"<div class='card'><div style='text-align:center;padding:20px'><b>{v['titulo']}</b><br><small style='opacity:0.6'>{v['descripcion']}</small><br><a href='{v.get('link')}' target='_blank' class='btn btn-p' style='margin-top:10px'>▶️ VER EN TIKTOK</a></div></div>"
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto;padding-bottom:90px}} </style><a href='/' class='btn' style='background:#333'>← Inicio</a><div style='display:flex;justify-content:space-between;align-items:center'><h2>🎬 Clips y Tutoriales</h2>{admin_add}</div>{html}{widget_bot()}"

@app.route('/subir-video', methods=['GET','POST'])
def subir_video():
    if not es_admin(): return redirect('/admin')
    if request.method=='POST':
        titulo=request.form['titulo'][:60]; descripcion=request.form['descripcion'][:200]; tipo=request.form['tipo']; link=request.form.get('link','').strip(); filename=None
        file = request.files.get('video')
        if file and file.filename!='':
            ext=file.filename.rsplit('.',1)[-1].lower()
            if ext in ALLOWED_EXT:
                filename=f"{int(datetime.now().timestamp())}_{secure_filename(file.filename)}"
                file.save(os.path.join(UPLOAD_FOLDER, filename))
        if not filename and not link:
            return "Tienes que subir archivo O pegar link"
        videos_dinamicos = []
        if os.path.exists(VIDEOS_FILE):
            try: videos_dinamicos = json.load(open(VIDEOS_FILE,"r",encoding="utf-8"))
            except: videos_dinamicos = []
        videos_dinamicos.append({"id":str(int(datetime.now().timestamp())),"titulo":titulo,"descripcion":descripcion,"tipo":tipo,"file":filename,"link":link,"fecha":datetime.now().strftime("%d/%m/%Y")})
        json.dump(videos_dinamicos, open(VIDEOS_FILE,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
        return redirect('/videos')
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto;padding-bottom:90px}} </style><a href='/videos' class='btn' style='background:#333'>← Volver</a><div class='card'><h2>📤 Subir Clip / Tutorial</h2><form method='post' enctype='multipart/form-data'><input name='titulo' placeholder='Título' required><select name='tipo'><option value='clip'>🎮 Clip / Jugada</option><option value='tutorial'>📚 Tutorial</option></select><textarea name='descripcion' placeholder='Descripción corta'></textarea><input type='file' name='video' accept='video/*' style='background:white;color:black'><input name='link' placeholder='Link TikTok/YouTube'><button class='btn btn-p' style='width:100%;margin-top:12px'>✅ PUBLICAR</button></form></div>{widget_bot()}"

@app.route('/borrar-video/<id>')
def borrar_video(id):
    if not es_admin(): return redirect('/admin')
    if id in [x['id'] for x in VIDEOS_FIJOS]:
        return "Este video es fijo, no se puede borrar (está en VIDEOS_FIJOS)"
    videos=[]
    if os.path.exists(VIDEOS_FILE):
        try: videos = json.load(open(VIDEOS_FILE,"r",encoding="utf-8"))
        except: videos=[]
    for v in videos:
        if v['id']==id and v.get('file'):
            try: os.remove(os.path.join(UPLOAD_FOLDER, v['file']))
            except: pass
    videos=[v for v in videos if v['id']!=id]
    json.dump(videos, open(VIDEOS_FILE,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
    return redirect('/videos')

@app.route('/registro', methods=['GET','POST'])
def registro():
    duos=cargar_duos()
    if request.method=='POST':
        if len(duos)>=MAX_DUOS: return "<script>alert('Cupo lleno');location='/registro'</script>"
        nuevo={"id":str(int(datetime.now().timestamp())),"nombre":request.form['nombre'][:30],"duo":request.form['duo'][:30],"id1":request.form['id1'][:30],"id2":request.form['id2'][:30],"fecha":datetime.now().strftime("%d/%m %H:%M")}
        ids_exist=[d['id1'] for d in duos]+[d['id2'] for d in duos]
        if nuevo['id1'] in ids_exist or nuevo['id2'] in ids_exist:
            return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;padding:20px;text-align:center}} </style><div class='card'><h3 style='color:#ff4444'>¡Ese ID ya está registrado!</h3><a href='/registro' class='btn btn-p'>Volver</a></div>{widget_bot()}"
        duos.append(nuevo); guardar_duos(duos); return redirect('/registro')
    cupo=len(duos)
    form_html=f"<div class='card' style='text-align:center;background:#ff000022'><h2>🔒 CUPO LLENO</h2></div>" if cupo>=MAX_DUOS else f"<div class='card'><h3>📝 Registrar mi Dúo ({cupo}/{MAX_DUOS})</h3><form method='post'><input name='nombre' placeholder='Tu nombre' required><input name='duo' placeholder='Nombre del Dúo' required><input name='id1' placeholder='ID Jugador 1' required><input name='id2' placeholder='ID Jugador 2' required><button class='btn btn-p' style='width:100%;margin-top:10px'>✅ INSCRIBIRNOS</button></form></div>"
    lista="".join([f"<div class='card' style='padding:10px 14px'><b>{i+1}. {d['duo']}</b><br><small>{d['id1']} + {d['id2']} | {d['nombre']}</small></div>" for i,d in enumerate(duos)]) or "<div class='card' style='text-align:center;opacity:0.6'>Aún no hay dúos</div>"
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto;padding-bottom:90px}} </style><a href='/' class='btn' style='background:#333'>← Volver</a><h2 style='text-align:center;color:#a855f7'>🏆 TORNEO 12 DÚOS - {cupo}/{MAX_DUOS}</h2>{form_html}{lista}{widget_bot()}"

@app.route('/borrar-duos')
def borrar_duos():
    if not es_admin(): return redirect('/admin')
    guardar_duos([]); return redirect('/registro')

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method=='POST':
        if request.form.get('password','').strip().lower()==PASSWORD.lower():
            session['admin']=True; return redirect('/')
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;text-align:center;padding:20px;padding-bottom:90px}} </style><div class='card'><h2>🔒 Admin</h2><form method='post'><input type='password' name='password' placeholder='Contraseña'><br><button class='btn btn-p'>Entrar</button></form></div>{widget_bot()}"

@app.route('/logout')
def logout(): session.pop('admin',None); return redirect('/')
@app.route('/nuevo', methods=['GET','POST'])
def nuevo():
    if not es_admin(): return redirect('/admin')
    if request.method=='POST':
        ev=cargar(); ev.append({"id":str(int(datetime.now().timestamp())),"titulo":request.form['titulo'],"fecha":request.form['fecha'],"lugar":request.form['lugar'],"estado":request.form['estado'],"descripcion":request.form['descripcion'],"marcador":request.form['marcador']}); guardar(ev); return redirect('/')
    return f"<meta name='viewport' content='width=device-width'><style>{estilos()} body{{color:white;padding:20px;max-width:600px;margin:auto;padding-bottom:90px}} textarea{{width:100%;padding:12px;border-radius:10px;box-sizing:border-box}} </style><div class='card'><h2>Nuevo Evento</h2><form method='post'><input name='titulo' placeholder='Titulo' required><input name='fecha' type='date' required><input name='lugar' placeholder='Lugar' required><select name='estado' style='width:100%;padding:12px;border-radius:10px;margin:8px 0'><option>proximo</option><option>vivo</option><option>finalizado</option></select><textarea name='descripcion' placeholder='Descripcion'></textarea><input name='marcador' placeholder='Marcador'><button class='btn btn-p' style='width:100%;margin-top:10px'>Guardar</button></form></div>{widget_bot()}"
