from flask import Flask, request, redirect, session
import json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "los-toxicos-2024-secret"
DATA_FILE = "eventos.json"
PASSWORD = "toxicos-1.0"

def cargar():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def es_admin():
    return session.get('admin') == True

def footer_redes():
    return """
    <div style='margin-top:40px;padding:25px;background:#1a1a1a;border-radius:18px;text-align:center;border:1px solid #333'>
        <h3 style='color:#00ff88;margin-bottom:5px'>🔥 REDES OFICIALES 🔥</h3>
        <p style='opacity:0.6;font-size:13px;margin-top:0'>Sigue a toda la banda tóxica</p>
        <div style='text-align:left;background:#222;padding:15px;border-radius:12px;margin:15px 0'>
            <b style='color:#00ff88'>☠️ CUENTA OFICIAL:</b><br>
            <a href='https://www.tiktok.com/@toxicos.de.bermuda' target='_blank' style='color:white;text-decoration:none;background:black;padding:8px 14px;border-radius:20px;display:inline-block;margin-top:8px;border:1px solid #00ff88'>🎵 @toxicos.de.bermuda - TÓXICOS DE BERMUDA</a>
        </div>
        <div style='text-align:left;background:#222;padding:15px;border-radius:12px;margin:15px 0'>
            <b style='color:#888'>👑 INTEGRANTES:</b><br>
            <div style='display:flex;flex-direction:column;gap:8px;margin-top:8px'>
                <a href='https://www.tiktok.com/@hsrramses' target='_blank' style='color:white;text-decoration:none'>🎵 HSRRAMSES - @hsrramses</a>
                <a href='https://www.tiktok.com/@botsto19' target='_blank' style='color:white;text-decoration:none'>🎵 BOSTO - @botsto19</a>
                <a href='https://www.tiktok.com/@ronan7538' target='_blank' style='color:white;text-decoration:none'>🎵 RONAN - @ronan7538</a>
            </div>
        </div>
        <div style='display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-top:20px'>
            <a href='https://www.facebook.com/profile.php?id=100024266709108' target='_blank' style='text-decoration:none;background:#1877F2;color:white;padding:12px 20px;border-radius:25px;font-weight:bold'>📘 Facebook</a>
            <a href='https://chat.whatsapp.com/KlGw8PxxQYWD0xYLuBlZpk' target='_blank' style='text-decoration:none;background:#25D366;color:white;padding:12px 20px;border-radius:25px;font-weight:bold'>💬 WhatsApp Grupo</a>
        </div>
        <p style='margin-top:20px;opacity:0.4;font-size:11px'>☠️ LOS TÓXICOS DE BERMUDA ☠️<br>Zapopan, Jalisco - Liga Oficial</p>
    </div>
    """

@app.route('/')
def home():
    eventos = cargar()
    eventos = sorted(eventos, key=lambda x: x.get('fecha',''), reverse=True)
    admin_btn = "<a href='/admin'><button>🔒 Admin</button></a>" if not es_admin() else "<a href='/logout'><button style='background:#ff4444;color:white'>Salir</button></a> <a href='/nuevo'><button>+ Nuevo</button></a>"
    html_eventos = ""
    for e in eventos:
        editar_link = f"<br><a href='/editar/{e['id']}' style='color:#00ff88'>✏️ Editar</a> | <a href='/eliminar/{e['id']}' style='color:#ff6666'>🗑️ Eliminar</a>" if es_admin() else ""
        estado_color = "#ff4444" if e['estado']=='vivo' else "#00ff88" if e['estado']=='finalizado' else "#888"
        html_eventos += f"""
        <div style='background:#1e1e1e;padding:15px;border-radius:12px;margin:15px 0;border-left:4px solid #00ff88'>
            <div style='display:flex;justify-content:space-between'><b>{e['titulo']}</b><span style='background:{estado_color};padding:4px 8px;border-radius:6px;font-size:11px;color:black'>{e['estado'].upper()}</span></div>
            <p>📅 {e['fecha']} | 📍 {e['lugar']}</p>
            <p>{e['descripcion']}</p>
            <b style='color:#00ff88'>{e.get('marcador','')}</b>
            {editar_link}
            <br><br><a href='https://wa.me/?text=Evento LOS TOXICOS: {e['titulo']} el {e['fecha']} en {e['lugar']} - Mira: https://los-toxicos.onrender.com' target='_blank' style='color:#25D366'>📲 Compartir</a>
        </div>
        """
    if not html_eventos:
        html_eventos = "<p style='text-align:center;opacity:0.6;padding:20px'>No hay eventos aún. ¡Mientras siguenos en TikTok! 👇</p>"
    return f"""
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>LOS TOXICOS DE BERMUDA</title>
    <style>body{{font-family:sans-serif;background:#0f0f0f;color:white;padding:20px;max-width:600px;margin:auto}} button{{background:#00ff88;color:black;padding:10px 16px;border:none;border-radius:8px;font-weight:bold}} h1{{color:#00ff88;text-align:center}}</style>
    <h1>☠️ TÓXICOS DE BERMUDA ☠️</h1>
    <p style='text-align:center;opacity:0.6;margin-top:-10px'>LIGA OFICIAL - ZAPOPAN</p>
    <div style='display:flex;justify-content:space-between;align-items:center'><h2>Eventos ({len(eventos)})</h2>{admin_btn}</div>
    {html_eventos}
    {footer_redes()}
    """

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        escrita = request.form.get('password','').strip()
        if escrita.lower() == PASSWORD.lower():
            session['admin'] = True
            return redirect('/')
        else:
            return f"""
            <meta name='viewport' content='width=device-width'>
            <body style='background:#0f0f0f;color:white;text-align:center;padding:20px;font-family:sans-serif'>
            <h3 style='color:#ff6666'>Contraseña incorrecta</h3>
            <a href='/admin' style='color:#00ff88'>Intentar de nuevo</a>
            </body>
            """
    return """
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{font-family:sans-serif;background:#0f0f0f;color:white;padding:20px;text-align:center} input{padding:14px;width:85%;border-radius:8px;border:none;margin:15px;font-size:16px} button{background:#00ff88;padding:14px 30px;border:none;border-radius:8px;font-weight:bold;font-size:16px}</style>
    <h2>🔒 Admin Los Tóxicos</h2>
    <p>Escribe la contraseña</p>
    <form method='post'>
    <input type='password' name='password' placeholder='••••••••••'><br>
    <button type='submit'>Entrar</button>
    </form>
    <br><br><a href='/' style='color:#00ff88'>Volver</a>
    """

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

@app.route('/nuevo', methods=['GET','POST'])
def nuevo():
    if not es_admin():
        return redirect('/admin')
    if request.method == 'POST':
        eventos = cargar()
        eventos.append({"id": str(int(datetime.now().timestamp())),"titulo": request.form['titulo'],"fecha": request.form['fecha'],"lugar": request.form['lugar'],"estado": request.form['estado'],"descripcion": request.form['descripcion'],"marcador": request.form['marcador']})
        guardar(eventos)
        return redirect('/')
    return form_html("Nuevo Evento")

@app.route('/editar/<id>', methods=['GET','POST'])
def editar(id):
    if not es_admin():
        return redirect('/admin')
    eventos = cargar()
    evento = next((x for x in eventos if x['id']==id), None)
    if not evento:
        return "No encontrado", 404
    if request.method == 'POST':
        evento['titulo']=request.form['titulo'];evento['fecha']=request.form['fecha'];evento['lugar']=request.form['lugar'];evento['estado']=request.form['estado'];evento['descripcion']=request.form['descripcion'];evento['marcador']=request.form['marcador']
        guardar(eventos)
        return redirect('/')
    return form_html("Actualizar", evento)

@app.route('/eliminar/<id>')
def eliminar(id):
    if not es_admin():
        return redirect('/admin')
    eventos = cargar()
    eventos = [x for x in eventos if x['id']!=id]
    guardar(eventos)
    return redirect('/')

def form_html(titulo_form, e=None):
    t = e['titulo'] if e else '';f = e['fecha'] if e else '';l = e['lugar'] if e else '';d = e['descripcion'] if e else '';m = e['marcador'] if e else '';est = e['estado'] if e else 'proximo'
    return f"""
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{{font-family:sans-serif;background:#0f0f0f;color:white;padding:20px}} input,select,textarea{{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:none}} button{{background:#00ff88;padding:12px;width:100%;border:none;border-radius:8px;font-weight:bold}}</style>
    <h2>{titulo_form}</h2>
    <form method='post'>
    <input name='titulo' value='{t}' placeholder='Nombre' required>
    <input name='fecha' type='date' value='{f}' required>
    <input name='lugar' value='{l}' placeholder='Lugar' required>
    <select name='estado'><option value='proximo' {'selected' if est=='proximo' else ''}>Proximo</option><option value='vivo' {'selected' if est=='vivo' else ''}>En Vivo</option><option value='finalizado' {'selected' if est=='finalizado' else ''}>Finalizado</option></select>
    <textarea name='descripcion' placeholder='Descripcion'>{d}</textarea>
    <input name='marcador' value='{m}' placeholder='Marcador'>
    <button type='submit'>Guardar</button>
    </form>
    <br><a href='/' style='color:#00ff88'>Volver</a>
    """
