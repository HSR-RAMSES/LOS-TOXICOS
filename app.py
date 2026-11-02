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

@app.route('/')
def home():
    eventos = cargar()
    eventos = sorted(eventos, key=lambda x: x.get('fecha',''), reverse=True)
    admin_btn = "<a href='/admin'><button>🔒 Admin</button></a>" if not es_admin() else "<a href='/logout'><button style='background:red;color:white'>Salir Admin</button></a> <a href='/nuevo'><button>+ Nuevo Evento</button></a>"
    
    html_eventos = ""
    for e in eventos:
        editar_link = f"<a href='/editar/{e['id']}' style='color:#00ff88'>✏️ Editar</a> | <a href='/eliminar/{e['id']}' style='color:red'>🗑️ Eliminar</a>" if es_admin() else ""
        estado_color = "red" if e['estado']=='vivo' else "green" if e['estado']=='finalizado' else "#555"
        html_eventos += f"""
        <div style='background:#1e1e1e;padding:15px;border-radius:12px;margin:15px 0;border-left:4px solid #00ff88'>
            <div style='display:flex;justify-content:space-between'><b>{e['titulo']}</b><span style='background:{estado_color};padding:4px 8px;border-radius:6px;font-size:11px'>{e['estado'].upper()}</span></div>
            <p>📅 {e['fecha']} | 📍 {e['lugar']}</p>
            <p>{e['descripcion']}</p>
            <b style='color:#00ff88'>{e.get('marcador','')}</b><br><br>
            {editar_link}
            <br><a href='https://wa.me/?text=Evento LOS TOXICOS: {e['titulo']} el {e['fecha']} en {e['lugar']} - Mira: https://los-toxicos.onrender.com' target='_blank' style='color:#25D366'>📲 Compartir por WhatsApp</a>
        </div>
        """
    if not html_eventos:
        html_eventos = "<p style='text-align:center;opacity:0.6'>No hay eventos aún. Entra como admin para crear.</p>"

    return f"""
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <title>LOS TOXICOS</title>
    <style>body{{font-family:sans-serif;background:#0f0f0f;color:white;padding:20px;max-width:600px;margin:auto}} button{{background:#00ff88;color:black;padding:10px 16px;border:none;border-radius:8px;font-weight:bold;cursor:pointer}} h1{{color:#00ff88;text-align:center}}</style>
    <h1>☠️ LIGA LOS TÓXICOS ☠️</h1>
    <div style='display:flex;justify-content:space-between;align-items:center'>
        <h2>Eventos ({len(eventos)})</h2>
        {admin_btn}
    </div>
    {html_eventos}
    <p style='text-align:center;margin-top:30px;opacity:0.5'>Contraseña admin solo para el encargado</p>
    """

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['admin'] = True
            return redirect('/')
        else:
            return "<h3 style='color:red'>Contraseña incorrecta</h3><a href='/admin'>Intentar de nuevo</a>"
    return """
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{font-family:sans-serif;background:#0f0f0f;color:white;padding:20px;text-align:center} input{padding:12px;width:80%;border-radius:8px;border:none;margin:10px} button{background:#00ff88;padding:12px 20px;border:none;border-radius:8px;font-weight:bold}</style>
    <h2>🔒 Admin Los Tóxicos</h2>
    <form method='post'>
    <input type='password' name='password' placeholder='Contraseña'><br>
    <button type='submit'>Entrar</button>
    </form>
    <br><a href='/' style='color:#00ff88'>Volver</a>
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
        nuevo_ev = {
            "id": str(int(datetime.now().timestamp())),
            "titulo": request.form['titulo'],
            "fecha": request.form['fecha'],
            "lugar": request.form['lugar'],
            "estado": request.form['estado'],
            "descripcion": request.form['descripcion'],
            "marcador": request.form['marcador']
        }
        eventos.append(nuevo_ev)
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
        evento['titulo']=request.form['titulo']
        evento['fecha']=request.form['fecha']
        evento['lugar']=request.form['lugar']
        evento['estado']=request.form['estado']
        evento['descripcion']=request.form['descripcion']
        evento['marcador']=request.form['marcador']
        guardar(eventos)
        return redirect('/')
    return form_html("Actualizar Evento", evento)

@app.route('/eliminar/<id>')
def eliminar(id):
    if not es_admin():
        return redirect('/admin')
    eventos = cargar()
    eventos = [x for x in eventos if x['id']!=id]
    guardar(eventos)
    return redirect('/')

def form_html(titulo_form, e=None):
    t = e['titulo'] if e else ''
    f = e['fecha'] if e else ''
    l = e['lugar'] if e else ''
    d = e['descripcion'] if e else ''
    m = e['marcador'] if e else ''
    est = e['estado'] if e else 'proximo'
    return f"""
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{{font-family:sans-serif;background:#0f0f0f;color:white;padding:20px}} input,select,textarea{{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:none}} button{{background:#00ff88;padding:12px;width:100%;border:none;border-radius:8px;font-weight:bold}}</style>
    <h2>{titulo_form}</h2>
    <form method='post'>
    <input name='titulo' placeholder='Nombre del evento' value='{t}' required>
    <input name='fecha' type='date' value='{f}' required>
    <input name='lugar' placeholder='Lugar / Cancha' value='{l}' required>
    <select name='estado'>
      <option value='proximo' {'selected' if est=='proximo' else ''}>Proximo</option>
      <option value='vivo' {'selected' if est=='vivo' else ''}>En Vivo</option>
      <option value='finalizado' {'selected' if est=='finalizado' else ''}>Finalizado</option>
    </select>
    <textarea name='descripcion' placeholder='Descripcion del evento'> {d}</textarea>
    <input name='marcador' placeholder='Marcador ej: 2-1' value='{m}'>
    <button type='submit'>Guardar</button>
    </form>
    <br><a href='/' style='color:#00ff88'>Volver</a>
    """
