from flask import Flask, request, redirect
import json, os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "eventos.json"

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

@app.route('/')
def home():
    eventos = cargar()
    eventos = sorted(eventos, key=lambda x: x.get('fecha',''), reverse=True)
    html = ""
    for e in eventos:
        html += f"""
        <div style='background:#1e1e1e;padding:15px;border-radius:12px;margin:15px 0;border-left:4px solid #00ff88'>
            <b>{e['titulo']}</b> - {e['estado'].upper()}<br>
            {e['fecha']} | {e['lugar']}<br>
            {e['descripcion']}<br>
            <b>{e.get('marcador','')}</b><br>
            <a href='/editar/{e['id']}' style='color:#00ff88'>Actualizar</a>
        </div>
        """
    if not html:
        html = "<p style='text-align:center;opacity:0.6'>No hay eventos aún. Crea el primero!</p>"

    return f"""
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{{font-family:sans-serif;background:#0f0f0f;color:white;padding:20px}} 
    button{{background:#00ff88;color:black;padding:12px;border:none;border-radius:8px;font-weight:bold;cursor:pointer}}
    h1{{color:#00ff88;text-align:center}}</style>
    <h1>☠️ LIGA LOS TOXICOS ☠️</h1>
    <div style='display:flex;justify-content:space-between;align-items:center'>
        <h2>Eventos ({len(eventos)})</h2>
        <a href='/nuevo'><button>+ Nuevo Evento</button></a>
    </div>
    {html}
    """

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
    <textarea name='descripcion' placeholder='Descripcion'>{d}</textarea>
    <input name='marcador' placeholder='Marcador ej: 2-1' value='{m}'>
    <button type='submit'>Guardar Evento</button>
    </form>
    <br><a href='/' style='color:#00ff88'>Volver</a>
    """

@app.route('/nuevo', methods=['GET','POST'])
def nuevo():
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

if __name__ == '__main__':
    app.run()
