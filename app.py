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
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# TUS LINKS REALES
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
def serve_video(filename): return send_from_directory(UPLOAD_FOLDER, filename)

def cargar(f, default=[]):
    if not os.path.exists(f): return default
    try: return json.load(open(f,"r",encoding="utf-8"))
    except: return default
def guardar(f,d): json.dump(d, open(f,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
def es_admin(): return session.get('admin')==True
def get_youtube_id(url):
    if not url: return None
    m = re.search(r'(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{6,})', url)
    return m.group(1) if m else None

def widget_bot_hsr():
    return """
    <div id='bot-hsr-btn' style='position:fixed;bottom:20px;right:20px;z-index:9999;background:#a855f7;color:white;padding:14px 20px;border-radius:30px;font-weight:bold;box-shadow:0 0 20px #a855f7aa;cursor:pointer;display:flex;align-items:center;gap:8px' onclick='toggleBot()'>🤖 BOT-HSR</div>
    <div id='bot-hsr-chat' style='display:none;position:fixed;bottom:85px;right:15px;z-index:9999;width:340px;max-width:90vw;height:420px;background:#141023;border:1px solid #a855f7;border-radius:16px;box-shadow:0 0 30px rgba(168,85,247,0.4);overflow:hidden;flex-direction:column'>
        <div style='background:#a855f7;padding:12px 15px;display:flex;justify-content:space-between;align-items:center;color:white'><div><b>🤖 BOT-HSR</b><br><small style='opacity:0.8'>HSR Ramses te responde</small></div><span onclick='toggleBot()' style='cursor:pointer;font-size:20px'>✕</span></div>
        <div id='bot-messages' style='flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px;background:#0a0614'></div>
        <div style='padding:10px;background:#141023'><input id='bot-name' placeholder='Tu nombre' style='padding:10px;border-radius:8px;border:none;width:100%;box-sizing:border-box;margin-bottom:6px'><div style='display:flex;gap:6px'><input id='bot-input' placeholder='Escribe tu duda...' style='flex:1;padding:10px;border-radius:8px;border:none'><button onclick='sendBot()' style='background:#a855f7;border:none;color:white;padding:10px 14px;border-radius:8px;font-weight:bold;cursor:pointer'>➤</button></div></div>
    </div>
    <script>
    let chatId = localStorage.getItem('hsr_chat_id') || null; let open = false;
    function toggleBot(){ open = !open; document.getElementById('bot-hsr-chat').style.display = open ? 'flex' : 'none'; if(open) loadBot(); }
    function addMsg(text, from){ const div = document.createElement('div'); div.style.cssText = from=='user' ? 'align-self:flex-end;background:#a855f7;color:white;padding:8px 12px;border-radius:14px 14px 0 14px;max-width:80%;font-size:13px' : 'align-self:flex-start;background:#222;color:white;padding:8px 12px;border-radius:14px 14px 14px 0;max-width:80%;font-size:13px;border:1px solid #a855f733'; div.innerText = text; document.getElementById('bot-messages').appendChild(div); document.getElementById('bot-messages').scrollTop = 99999; }
    async function loadBot(){ if(!chatId) return; const r = await fetch('/chat/get?chat_id='+chatId); const data = await r.json(); document.getElementById('bot-messages').innerHTML=''; data.messages.forEach(m=> addMsg(m.text, m.from)); }
    async function sendBot(){ const name = document.getElementById('bot-name').value || 'Anon'; const text = document.getElementById('bot-input').value; if(!text.trim()) return; addMsg(text,'user'); document.getElementById('bot-input').value=''; const r = await fetch('/chat/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({chat_id:chatId, name:name, text:text})}); const data = await r.json(); chatId = data.chat_id; localStorage.setItem('hsr_chat_id', chatId); localStorage.setItem('hsr_chat_name', name); setTimeout(loadBot, 500); }
    document.getElementById('bot-input')?.addEventListener('keydown', e=>{ if(e.key==='Enter') sendBot(); }); document.getElementById('bot-name').value = localStorage.getItem('hsr_chat_name') || ''; setInterval(()=>{ if(open && chatId) loadBot(); }, 3000);
    </script>
    """

def base_html(content):
    estilos = """
    body{background:linear-gradient(rgba(0,0,0,0.7),rgba(10,5,20,0.85)),url('/fondo.jpg');background-size:cover;background-attachment:fixed;background-position:center top;min-height:100vh;margin:0;}
    .card{background:rgba(20,15,35,0.92);backdrop-filter:blur(8px);border:1px solid rgba(168,85,247,0.3);box-shadow:0 0 20px rgba(168,85,247,0.15);border-radius:16px;padding:16px;margin:14px 0;}
    .btn{display:inline-block;padding:12px 22px;border-radius:30px;text-decoration:none;font-weight:bold;margin:6px;color:white;border:none;cursor:pointer;text-align:center}
    .btn-p{background:#a855f7;box-shadow:0 0 15px #a855f780} .wa{background:#25D366} .fb{background:#1877F2} .tt{background:#000;border:1px solid #a855f7} .tt2{background:#1a1a1a;border:1px solid #555}
    input,textarea,select{width:100%;padding:13px;margin:7px 0;border-radius:10px;border:none;box-sizing:border-box}
    video,iframe{width:100%;border-radius:12px;background:#000;border:none}
    """
    return f"<meta name='viewport' content='width=device-width, initial-scale=1'><style>{estilos} body{{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto;padding-bottom:90px}} h1{{color:#a855f7;text-align:center;text-shadow:0 0 18px #a855f7}} </style>{content}{widget_bot_hsr()}"

@app.route('/')
def home():
    eventos=cargar(DATA_FILE)
    # Si no hay eventos, ponemos unos por defecto para que no se vea vacío
    if not eventos:
        eventos = [
            {"titulo":"Bienvenidos Tóxicos de Bermuda","fecha":"2025","lugar":"Zapopan, Jalisco","descripcion":"¡La casa oficial de HSR Ramses y los Tóxicos! Aquí verás torneos, clips y tutoriales.","marcador":"HSR RAMSES EDITION"}
        ]
    duos=cargar(DUOS_FILE)
    admin_btn = f"<a href='/admin'><button class='btn' style='background:#a855f7'>🔒 Admin</button></a>" if not es_admin() else f"<a href='/mensajes'><button class='btn' style='background:#ffaa00'>💬 Mensajes</button></a> <a href='/nuevo'><button class='btn btn-p'>+ Evento</button></a> <a href='/logout'><button class='btn' style='background:#ff4444'>Salir</button></a>"
    html_e = "".join([f"<div class='card' style='border-left:4px solid #a855f7'><b>{e['titulo']}</b> - {e['fecha']}<br><small style='opacity:0.7'>{e['lugar']}</small><br><b style='color:#a855f7'>{e.get('marcador','')}</b><br>{e['descripcion']}</div>" for e in eventos])
    cupo = f"{len(duos)}/{MAX_DUOS} DÚOS"
    lista_home = "".join([f"<div style='padding:6px 10px;margin:4px 0;background:rgba(255,255,255,0.06);border-radius:8px;font-size:13px'>{i+1}. <b>{d['duo']}</b> | {d['id1']} + {d['id2']}</div>" for i,d in enumerate(duos)]) if duos else "<small style='opacity:0.5'>Aún no hay dúos - ¡Sé el primero!</small>"
    
    contenido = f"""
    <h1>☠️ TÓXICOS DE<br>BERMUDA ☠️</h1><p style='text-align:center;opacity:0.7;letter-spacing:2px;font-size:13px'>HSR RAMSES EDITION</p>
    <div style='display:flex;justify-content:space-between;align-items:center'><h2>Eventos</h2>{admin_btn}</div>
    {html_e}
    <div class='card' style='text-align:center'>
        <h3 style='color:#a855f7;margin:0 0 12px'>🏆 TORNEO {cupo}</h3>
        <a href='/registro' class='btn btn-p'>📝 INSCRIBIR DÚO</a>
        <a href='/videos' class='btn' style='background:#333'>🎬 VER CLIPS Y TUTORIALES</a>
        <div style='text-align:left;margin-top:15px;max-height:220px;overflow:auto'>{lista_home}</div>
    </div>
    <div class='card' style='text-align:center'>
        <h3 style='color:#a855f7'>🔥 SÍGUENOS EN TODAS LAS REDES 🔥</h3>
        <a href='{LINK_WHATSAPP}' target='_blank' class='btn wa'>💬 WhatsApp Tóxicos</a>
        <a href='{LINK_FACEBOOK}' target='_blank' class='btn fb'>👥 Facebook</a><br>
        <a href='{LINK_TIKTOK_TOXICOS}' target='_blank' class='btn tt'>☠️ TÓXICOS DE BERMUDA</a>
        <a href='{LINK_TIKTOK_HSR}' target='_blank' class='btn tt2'>👑 HSRRAMSES</a>
        <a href='{LINK_TIKTOK_BOSTO}' target='_blank' class='btn tt2'>⚔️ BOSTO19</a>
        <a href='{LINK_TIKTOK_RONAN}' target='_blank' class='btn tt2'>🔥 RONAN7538</a>
    </div>
    """
    return base_html(contenido)

# --- CHAT ---
@app.route('/chat/send', methods=['POST'])
def chat_send():
    data = request.get_json(); chat_id = data.get('chat_id'); text = data.get('text','').strip()[:500]; name = data.get('name','Anon')[:30]
    if not text: return jsonify({"error":"vacio"})
    chats = cargar(CHATS_FILE)
    if not chat_id:
        chat_id = str(int(datetime.now().timestamp()*1000))
        chats.append({"id":chat_id,"name":name,"last":datetime.now().strftime("%d/%m %H:%M"),"messages":[{"from":"user","text":text,"time":datetime.now().strftime("%H:%M")}]})
    else:
        for c in chats:
            if c['id']==chat_id: c['last']=datetime.now().strftime("%d/%m %H:%M"); c['name']=name; c['messages'].append({"from":"user","text":text,"time":datetime.now().strftime("%H:%M")}); break
        else: chats.append({"id":chat_id,"name":name,"last":datetime.now().strftime("%d/%m %H:%M"),"messages":[{"from":"user","text":text,"time":datetime.now().strftime("%H:%M")}]})
    guardar(CHATS_FILE, chats); return jsonify({"chat_id":chat_id})

@app.route('/chat/get')
def chat_get():
    chat_id = request.args.get('chat_id'); chats = cargar(CHATS_FILE)
    for c in chats:
        if c['id']==chat_id: return jsonify(c)
    return jsonify({"messages":[]})

@app.route('/chat/admin_send', methods=['POST'])
def chat_admin_send():
    if not es_admin(): return jsonify({"error":"no admin"})
    data = request.get_json(); chat_id = data.get('chat_id'); text = data.get('text','').strip()[:500]
    chats = cargar(CHATS_FILE)
    for c in chats:
        if c['id']==chat_id: c['messages'].append({"from":"admin","text":text,"time":datetime.now().strftime("%H:%M")})
    guardar(CHATS_FILE, chats); return jsonify({"ok":True})

@app.route('/mensajes')
def mensajes():
    if not es_admin(): return redirect('/admin')
    chats = cargar(CHATS_FILE); chats = sorted(chats, key=lambda x: x.get('last',''), reverse=True)
    html_chats = "".join([f"<div class='card' style='cursor:pointer' onclick=\"openChat('{c['id']}','{c['name']}')\"><b>{c['name']}</b> <small style='opacity:0.5'>{c['last']}</small><br><small>{c['messages'][-1]['text'][:40]}...</small></div>" for c in chats]) or "<div class='card' style='text-align:center'>No hay mensajes aún. Cuando alguien use el BOT-HSR aparecerá aquí.</div>"
    return base_html(f"<a href='/' class='btn' style='background:#333'>← Inicio</a><h2>💬 Mensajes BOT-HSR</h2><div style='display:flex;gap:10px;flex-wrap:wrap'><div style='flex:1;min-width:280px'>{html_chats}</div><div id='chat-view' style='flex:1.5;display:none;min-width:280px' class='card'><div id='chat-view-name' style='font-weight:bold;color:#a855f7'></div><div id='chat-view-msgs' style='height:300px;overflow:auto;display:flex;flex-direction:column;gap:6px;background:#0a0614;padding:10px;border-radius:10px'></div><div style='display:flex;gap:6px;margin-top:10px'><input id='admin-input' placeholder='Responde como HSR Ramses...'><button onclick='sendAdmin()' class='btn btn-p'>Enviar</button></div><div style='text-align:right'><a id='del-chat' href='#' style='color:#ff6666;font-size:12px'>Borrar chat</a></div></div></div><script>let curId=null;function openChat(id,name){{curId=id;document.getElementById('chat-view').style.display='block';document.getElementById('chat-view-name').innerText=name;document.getElementById('del-chat').href='/borrar-chat/'+id;loadAdminChat();}}async function loadAdminChat(){{if(!curId) return;const r=await fetch('/chat/get?chat_id='+curId);const data=await r.json();const cont=document.getElementById('chat-view-msgs');cont.innerHTML='';data.messages.forEach(m=>{{const d=document.createElement('div');d.style.cssText=m.from=='user'?'align-self:flex-start;background:#222;padding:8px 12px;border-radius:12px;max-width:80%;font-size:13px':'align-self:flex-end;background:#a855f7;padding:8px 12px;border-radius:12px;max-width:80%';d.innerText=m.from.toUpperCase()+': '+m.text;cont.appendChild(d);}});cont.scrollTop=9999;}}async function sendAdmin(){{const t=document.getElementById('admin-input').value;if(!t.trim()) return;await fetch('/chat/admin_send',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{chat_id:curId,text:t}})}});document.getElementById('admin-input').value='';loadAdminChat();}}setInterval(()=>{{if(curId) loadAdminChat();}},2000);</script>")

@app.route('/borrar-chat/<id>')
def borrar_chat(id):
    if not es_admin(): return redirect('/admin')
    guardar(CHATS_FILE, [c for c in cargar(CHATS_FILE) if c['id']!=id]); return redirect('/mensajes')

# --- VIDEOS ---
@app.route('/videos')
def pag_videos():
    videos=cargar(VIDEOS_FILE); admin_add = f"<a href='/subir-video'><button class='btn btn-p'>+ Subir Video</button></a>" if es_admin() else ""; html=""
    if not videos: html="<div class='card' style='text-align:center'>No hay clips aún</div>"
    else:
        for v in reversed(videos):
            yt=get_youtube_id(v.get('link','')); del_btn=f"<div style='text-align:right'><a href='/borrar-video/{v['id']}' style='color:#ff6666;font-size:12px'>Borrar</a></div>" if es_admin() else ""
            if yt: html+=f"<div class='card'><iframe height='280' src='https://www.youtube.com/embed/{yt}' allowfullscreen></iframe><b>{v['titulo']}</b>{del_btn}</div>"
            elif v.get('file'): html+=f"<div class='card'><video controls><source src='/uploads/videos/{v['file']}'></video><b>{v['titulo']}</b>{del_btn}</div>"
            else: html+=f"<div class='card'><b>{v['titulo']}</b><br><a href='{v.get('link')}' target='_blank' class='btn btn-p'>Ver Video</a>{del_btn}</div>"
    return base_html(f"<a href='/' class='btn' style='background:#333'>← Inicio</a><div style='display:flex;justify-content:space-between'><h2>🎬 Clips y Tutoriales</h2>{admin_add}</div>{html}")

@app.route('/subir-video', methods=['GET','POST'])
def subir_video():
    if not es_admin(): return redirect('/admin')
    if request.method=='POST':
        titulo=request.form['titulo'][:60]; desc=request.form['descripcion'][:200]; tipo=request.form['tipo']; link=request.form.get('link','').strip(); filename=None
        file=request.files.get('video')
        if file and file.filename!='':
            ext=file.filename.rsplit('.',1)[-1].lower()
            if ext in ALLOWED_EXT:
                filename=f"{int(datetime.now().timestamp())}_{secure_filename(file.filename)}"; file.save(os.path.join(UPLOAD_FOLDER, filename))
        if not filename and not link: return "Sube archivo o pega link"
        videos=cargar(VIDEOS_FILE); videos.append({"id":str(int(datetime.now().timestamp())),"titulo":titulo,"descripcion":desc,"tipo":tipo,"file":filename,"link":link,"fecha":datetime.now().strftime("%d/%m/%Y")}); guardar(VIDEOS_FILE, videos); return redirect('/videos')
    return base_html("<a href='/videos' class='btn' style='background:#333'>← Volver</a><div class='card'><h2>📤 Subir Video</h2><form method='post' enctype='multipart/form-data'><input name='titulo' placeholder='Título' required><select name='tipo'><option value='clip'>Clip</option><option value='tutorial'>Tutorial</option></select><textarea name='descripcion' placeholder='Descripción'></textarea><input type='file' name='video' accept='video/*' style='background:white;color:black'><input name='link' placeholder='O pega link YouTube/TikTok'><button class='btn btn-p' style='width:100%;margin-top:10px'>PUBLICAR</button></form></div>")

@app.route('/borrar-video/<id>')
def borrar_video(id):
    if not es_admin(): return redirect('/admin')
    videos=cargar(VIDEOS_FILE)
    for v in videos:
        if v['id']==id and v.get('file'):
            try: os.remove(os.path.join(UPLOAD_FOLDER, v['file']))
            except: pass
    guardar(VIDEOS_FILE, [v for v in videos if v['id']!=id]); return redirect('/videos')

@app.route('/registro', methods=['GET','POST'])
def registro():
    duos=cargar(DUOS_FILE)
    if request.method=='POST':
        if len(duos)>=MAX_DUOS: return "<script>alert('Cupo lleno');location='/registro'</script>"
        nuevo={"id":str(int(datetime.now().timestamp())),"nombre":request.form['nombre'][:30],"duo":request.form['duo'][:30],"id1":request.form['id1'][:30],"id2":request.form['id2'][:30],"fecha":datetime.now().strftime("%d/%m %H:%M")}
        ids_exist=[d['id1'] for d in duos]+[d['id2'] for d in duos]
        if nuevo['id1'] in ids_exist or nuevo['id2'] in ids_exist:
            return base_html("<div class='card'><h3 style='color:#ff4444'>¡Ese ID ya está registrado!</h3><a href='/registro' class='btn btn-p'>Volver</a></div>")
        duos.append(nuevo); guardar(DUOS_FILE, duos); return redirect('/registro')
    cupo=len(duos)
    form_html=f"<div class='card' style='text-align:center;background:#ff000022'><h2>🔒 CUPO LLENO - {MAX_DUOS} DÚOS</h2></div>" if cupo>=MAX_DUOS else f"<div class='card'><h3>📝 Registrar mi Dúo ({cupo}/{MAX_DUOS})</h3><form method='post'><input name='nombre' placeholder='Tu nombre' required><input name='duo' placeholder='Nombre del Dúo' required><input name='id1' placeholder='ID Jugador 1' required><input name='id2' placeholder='ID Jugador 2' required><button class='btn btn-p' style='width:100%'>✅ INSCRIBIRNOS</button></form></div>"
    lista="".join([f"<div class='card'><b>{i+1}. {d['duo']}</b><br><small>{d['id1']} + {d['id2']} | {d['nombre']}</small></div>" for i,d in enumerate(duos)]) or "<div class='card' style='text-align:center;opacity:0.6'>Aún no hay dúos</div>"
    return base_html(f"<a href='/' class='btn' style='background:#333'>← Volver</a><h2 style='text-align:center;color:#a855f7'>🏆 TORNEO 12 DÚOS - {cupo}/{MAX_DUOS}</h2>{form_html}{lista}")

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method=='POST':
        if request.form.get('password','').strip().lower()==PASSWORD.lower():
            session['admin']=True; return redirect('/')
    return base_html("<div class='card' style='text-align:center'><h2>🔒 Admin</h2><form method='post'><input type='password' name='password' placeholder='Contraseña: toxicos-1.0'><br><button class='btn btn-p'>Entrar</button></form></div>")

@app.route('/logout')
def logout(): session.pop('admin',None); return redirect('/')
@app.route('/borrar-duos')
def borrar_duos():
    if not es_admin(): return redirect('/admin')
    guardar(DUOS_FILE, []); return redirect('/registro')
@app.route('/nuevo', methods=['GET','POST'])
def nuevo():
    if not es_admin(): return redirect('/admin')
    if request.method=='POST':
        ev=cargar(DATA_FILE); ev.append({"id":str(int(datetime.now().timestamp())),"titulo":request.form['titulo'],"fecha":request.form['fecha'],"lugar":request.form['lugar'],"estado":request.form['estado'],"descripcion":request.form['descripcion'],"marcador":request.form['marcador']}); guardar(DATA_FILE, ev); return redirect('/')
    return base_html("<div class='card'><h2>Nuevo Evento</h2><form method='post'><input name='titulo' placeholder='Titulo' required><input name='fecha' type='date' required><input name='lugar' placeholder='Lugar' required><select name='estado'><option>proximo</option><option>vivo</option><option>finalizado</option></select><textarea name='descripcion' placeholder='Descripcion'></textarea><input name='marcador' placeholder='Marcador'><button class='btn btn-p' style='width:100%'>Guardar</button></form></div>")
