from flask import Flask, render_template_string, request, redirect
import json, os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "eventos.json"

# Cargar eventos
def cargar():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LOS TOXICOS - Eventos</title>
<style>
 body{font-family:sans-serif;background:#0f0f0f;color:white;margin:0;padding:20px}
 h1{color:#00ff88;text-align:center}
 .card{background:#1e1e1e;padding:15px;border-radius:12px;margin:15px 0;border-left:4px solid #00ff88}
 .estado{padding:4px 8px;border-radius:6px;font-size:12px}
 .proximo{background:#333} .vivo{background:red} .finalizado{background:green}
 input,select,textarea{width:100%;padding:10px;margin:5px 0;border-radius:8px;border:none}
 button{background:#00ff88;color:black;padding:12px;border:none;border-radius:8px;font-weight:bold;width:100%;cursor:pointer}
 a{color:#00ff88}
 .top{display:flex;justify-content:space-between;align-items:center}
</style>
</head>
<body>
<h1>☠️ LIGA LOS TÓXICOS ☠️</h1>
<div class="top">
 <h2>Eventos ({{eventos|length}})</h2>
 <a href="/nuevo"><button style="width:auto">+ Nuevo Evento</button></a>
</div>

{% for e in eventos %}
<div class="card">
  <div class="top">
    <h3>{{e.titulo}}</h3>
    <span class="estado {{e.estado}}">{{e.estado.upper()}}</span>
  </div>
  <p>📅 {{e.fecha}} | 📍 {{e.lugar}}</p>
  <p>{{e.descripcion}}</p>
  {% if e.marcador %}<p><b>Marcador:</b> {{e.marcador}}</p>{% endif %}
  <a href="/editar/{{e.id}}">Actualizar / Editar</a>
</div>
{% else %}
<p style="text-align:center;opacity:0.6">Aún no hay eventos. ¡Crea el primero!</p>
{% endfor %}

</body>
</html>
"""

FORM = """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{font-family:sans-serif;background:#0f0f0f;color:white;padding:20px} input,select,textarea{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:none} button{background:#00ff88;padding:12px;width:100%;border:none;border-radius:8px;font-weight:bold}</style>
</head>
<body>
<h2>{{titulo_form}}</h2>
<form method="post">
<input name="titulo" placeholder="Nombre del evento (ej: Toxicos vs Retros)" value="{{e.titulo if e else ''}}" required>
<input name="fecha" type="date" value="{{e.fecha if e else ''}}" required>
<input name="lugar" placeholder="Lugar / Cancha" value="{{e.lugar if e else ''}}" required>
<select name="estado">
  <option value="proximo" {% if e and e.estado=='proximo' %}selected{% endif %}>Próximo</option>
  <option value="vivo" {% if e and e.estado=='vivo' %}selected{% endif %}>En Vivo 🔴</option>
  <option value="finalizado" {% if e and e.estado=='finalizado' %}selected{% endif %}>Finalizado</option>
</select>
<textarea name="descripcion" placeholder="Descripción">{{e.descripcion if e else ''}}</textarea>
<input name="marcador" placeholder="Marcador (ej: 2-1)" value="{{e.marcador if e else ''}}">
<button type="submit">Guardar Evento</button>
</form>
<br><a href="/" style="color:#00ff88">← Volver</a>
</body>
</html>
"""

@app.route('/')
def home():
    eventos = cargar()
    eventos = sorted(eventos, key=lambda x: x['fecha'], reverse=True)
    return render_template_string(HTML, eventos=eventos)

@app.route('/nuevo', methods=['GET','POST'])
def nuevo():
    if request.method == 'POST':
        eventos = cargar()
        nuevo = {
            "id": str(int(datetime.now().timestamp())),
            "titulo": request.form['titulo'],
            "fecha": request.form['fecha'],
            "lugar": request.form['lugar'],
            "estado": request.form['estado'],
            "descripcion": request.form['descripcion'],
            "marcador": request.form['marcador']
        }
        eventos.append(nuevo)
        guardar(eventos)
        return redirect('/')
    return render_template_string(FORM, titulo_form="Nuevo Evento", e=None)

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
    return render_template_string(FORM, titulo_form="Actualizar Evento", e=evento)

if __name__ == '__main__':
    app.run()
"""

4. Dale **Commit changes**
5. Render se va a actualizar solo (1 minuto y vuelve a decir Live)

Y listo. Con eso ya puedes:

- Subir eventos desde tu celular
- Cambiar a "EN VIVO" cuando empiece el partido
- Poner marcador final

¿Quieres que también le ponga?
1. Que subas foto del flyer del evento
2. Que la gente vea los eventos sin poder editar (solo tú con contraseña)

Dime cuál quieres y te paso la versión 2 con contraseña de admin.
