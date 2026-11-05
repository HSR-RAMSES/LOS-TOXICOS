"""
navbar.py - Barra inferior estilo TikTok + chat de comunidad + perfiles + buscador.
Va en la MISMA carpeta que app.py. No toca tus rutas existentes.

Pestañas:   Reels (/videos)  💬 Chat (/comunidad)  🏆 Inscribir (/inscribir)  👤 Perfil (/perfil)
Arriba a la derecha:  inicio y 🔍 buscador (/buscar)
"""
import json, os, re
from datetime import datetime
from html import escape
from flask import request, redirect, session, jsonify

USUARIOS_FILE = "usuarios.json"
COMUNIDAD_FILE = "comunidad.json"
_H = {}  # funciones de app.py que se reciben en init_nav


# ---------- archivos ----------
def _leer(ruta, defecto):
    if not os.path.exists(ruta):
        return defecto
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return defecto


def _guardar(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)


def cargar_usuarios():
    return _leer(USUARIOS_FILE, [])


def guardar_usuarios(d):
    _guardar(USUARIOS_FILE, d)


def usuario_actual():
    uid = session.get("uid")
    if not uid:
        return None
    for u in cargar_usuarios():
        if u["ff_id"] == uid:
            return u
    return None


# ---------- barra ----------
CSS_NAV = """
.topbar{position:fixed;top:10px;right:10px;z-index:9998;display:flex;gap:6px}
.topbar a{width:38px;height:38px;border-radius:50%;background:rgba(20,15,35,.92);border:1px solid #a855f7;display:flex;align-items:center;justify-content:center;text-decoration:none;font-size:17px}
.nav{position:fixed;left:0;right:0;bottom:0;z-index:9998;height:62px;background:#0a0614;border-top:1px solid rgba(168,85,247,.45);display:flex}
.nav a{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;color:#8a8a99;text-decoration:none;font-size:11px;font-weight:bold}
.nav a span{font-size:22px;line-height:1}
.nav a.on{color:#a855f7}
.nav a.on span{filter:drop-shadow(0 0 6px #a855f7)}
#bot-hsr-btn{bottom:78px!important}
#bot-hsr-chat{bottom:140px!important}
body{padding-bottom:90px!important;padding-top:56px!important}
"""


def barra_nav(activo=""):
    items = [
        ("reels", "/videos", "🎬", "Reels"),
        ("chat", "/comunidad", "💬", "Chat"),
        ("inscribir", "/inscribir", "🏆", "Inscribir"),
        ("perfil", "/perfil", "👤", "Perfil"),
    ]
    links = ""
    for clave, href, icono, texto in items:
        clase = "on" if clave == activo else ""
        links += "<a href='%s' class='%s'><span>%s</span>%s</a>" % (href, clase, icono, texto)
    return ("<style>" + CSS_NAV + "</style>"
            "<div class='topbar'><a href='/'>🏠</a><a href='/buscar'>🔍</a></div>"
            "<nav class='nav'>" + links + "</nav>")


def pagina(contenido, activo="", bot=True):
    base = "body{font-family:sans-serif;color:white;padding:18px;max-width:650px;margin:auto}"
    widget = _H["widget_bot"]() if bot else ""
    return ("<meta name='viewport' content='width=device-width, initial-scale=1'>"
            "<style>" + _H["estilos"]() + base + "</style>" + contenido + barra_nav(activo) + widget)


# ---------- piezas de perfil ----------
def _avatar(u, size=64):
    ini = escape((u["nombre"][:1] or "?").upper())
    return ("<div style='width:%dpx;height:%dpx;border-radius:50%%;background:#a855f7;margin:auto;"
            "display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:%dpx;"
            "flex-shrink:0'>%s</div>") % (size, size, size // 2, ini)


def _miembros_html():
    us = cargar_usuarios()
    if not us:
        return "<small style='opacity:.5'>Aún no hay miembros. ¡Sé el primero!</small>"
    out = ""
    for u in reversed(us):
        out += ("<a href='/perfil/%s' style='text-decoration:none;color:white'>"
                "<div class='card' style='margin:6px 0;padding:10px;display:flex;align-items:center;gap:10px'>"
                "<div style='width:36px'>%s</div><div><b>%s</b><br><small style='opacity:.6'>ID: %s</small></div>"
                "</div></a>") % (escape(u["ff_id"]), _avatar(u, 36), escape(u["nombre"]), escape(u["ff_id"]))
    return out


def _tarjeta_perfil(u, propio):
    duo = None
    for d in _H["cargar_duos"]():
        if u["ff_id"] in (str(d.get("id1", "")), str(d.get("id2", ""))):
            duo = d
            break
    if duo:
        duo_html = "<div style='margin-top:10px'>🏆 Dúo: <b>%s</b></div>" % escape(str(duo.get("duo", "")))
    else:
        duo_html = "<div style='margin-top:10px;opacity:.6'>Sin dúo inscrito</div>"
    salir = "<a href='/perfil/salir' class='btn' style='background:#ff4444'>Salir</a>" if propio else ""
    return ("<div class='card' style='text-align:center'>%s<h2 style='margin:10px 0 2px'>%s</h2>"
            "<div style='opacity:.85'>🎮 ID Free Fire: <b>%s</b></div>"
            "<small style='opacity:.5'>Miembro desde %s</small>%s<div>%s</div></div>") % (
        _avatar(u, 80), escape(u["nombre"]), escape(u["ff_id"]), escape(u.get("fecha", "")), duo_html, salir)


def _seccion(titulo, items):
    if not items:
        return ""
    return "<h3 style='color:#a855f7'>%s</h3>%s" % (titulo, "".join(items))


# ---------- rutas ----------
def init_nav(app, estilos, widget_bot, cargar_videos, cargar_eventos, cargar_duos, es_admin, max_duos=12):
    _H.update(estilos=estilos, widget_bot=widget_bot, cargar_videos=cargar_videos,
              cargar_eventos=cargar_eventos, cargar_duos=cargar_duos, es_admin=es_admin)

    # ----- 3) Inscribir: eventos + dúos -----
    @app.route("/inscribir")
    def inscribir():
        eventos = cargar_eventos()
        duos = cargar_duos()
        aviso = ""
        if not usuario_actual():
            aviso = ("<div class='card' style='text-align:center'>Crea tu perfil con tu ID de Free Fire: "
                     "<a href='/perfil' style='color:#a855f7'>Registrarme</a></div>")
        ev = ""
        for e in eventos:
            ev += ("<div class='card' style='border-left:4px solid #a855f7'><b>%s</b> - %s<br><small>%s</small>"
                   "<br>%s</div>") % (escape(str(e.get("titulo", ""))), escape(str(e.get("fecha", ""))),
                                      escape(str(e.get("lugar", ""))), escape(str(e.get("descripcion", ""))))
        if not ev:
            ev = "<div class='card' style='text-align:center'>📭 No hay eventos aún</div>"
        lista = ""
        for i, d in enumerate(duos):
            lista += ("<div style='padding:6px 10px;margin:4px 0;background:rgba(255,255,255,0.06);"
                      "border-radius:8px;font-size:13px'>%d. <b>%s</b> | %s + %s</div>") % (
                i + 1, escape(str(d.get("duo", ""))), escape(str(d.get("id1", ""))), escape(str(d.get("id2", ""))))
        if not lista:
            lista = "<small style='opacity:.5'>Aún no hay dúos</small>"
        cont = ("<h2>🏆 Inscripciones</h2>%s"
                "<div class='card' style='text-align:center'><h3 style='color:#a855f7;margin:0 0 12px'>TORNEO %d/%d DÚOS</h3>"
                "<a href='/registro' class='btn btn-p'>📝 INSCRIBIR DÚO</a>"
                "<div style='text-align:left;margin-top:15px;max-height:220px;overflow:auto'>%s</div></div>"
                "<h3 style='color:#a855f7'>📅 Eventos</h3>%s") % (aviso, len(duos), max_duos, lista, ev)
        return pagina(cont, "inscribir")

    # ----- 2) Chat de la comunidad -----
    @app.route("/comunidad")
    def comunidad():
        u = usuario_actual()
        yo = escape(u["ff_id"]) if u else ""
        if u:
            caja = ("<div style='display:flex;gap:6px'><input id='txt' placeholder='Escribe a la comunidad...' maxlength='300'>"
                    "<button class='btn btn-p' onclick='enviar()' style='margin:7px 0'>➤</button></div>")
        else:
            caja = ("<div class='card' style='text-align:center'>Para escribir necesitas tu perfil: "
                    "<a href='/perfil' style='color:#a855f7'>Registrarme</a></div>")
        js = """<script>
const cont=document.getElementById('msgs'); const yo=cont.dataset.yo;
async function cargar(){
  const r=await fetch('/comunidad/get'); const data=await r.json();
  const abajo=cont.scrollTop+cont.clientHeight>=cont.scrollHeight-40;
  cont.innerHTML='';
  data.forEach(m=>{
    const mio=m.ff_id===yo; const d=document.createElement('div');
    d.style.cssText='max-width:80%;padding:8px 12px;font-size:13px;border-radius:14px;'+(mio?'align-self:flex-end;background:#a855f7;':'align-self:flex-start;background:#222;');
    const n=document.createElement('small'); n.style.opacity='.7'; n.innerText=(mio?'Tú':m.name)+' · '+m.time;
    const t=document.createElement('div'); t.innerText=m.text;
    d.appendChild(n); d.appendChild(t); cont.appendChild(d);
  });
  if(abajo) cont.scrollTop=cont.scrollHeight;
}
async function enviar(){
  const i=document.getElementById('txt'); const t=i.value.trim(); if(!t) return; i.value='';
  await fetch('/comunidad/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})});
  cargar(); setTimeout(()=>{cont.scrollTop=cont.scrollHeight;},300);
}
const inp=document.getElementById('txt'); if(inp) inp.addEventListener('keydown',e=>{if(e.key==='Enter') enviar();});
cargar(); setInterval(cargar,3000);
</script>"""
        cont = ("<h2>💬 Chat de la comunidad</h2>"
                "<div id='msgs' data-yo='%s' style='height:calc(100vh - 270px);min-height:220px;overflow:auto;display:flex;"
                "flex-direction:column;gap:6px;background:#0a0614;padding:10px;border-radius:12px;border:1px solid rgba(168,85,247,.3)'></div>"
                "%s%s") % (yo, caja, js)
        return pagina(cont, "chat", bot=False)

    @app.route("/comunidad/get")
    def comunidad_get():
        return jsonify(_leer(COMUNIDAD_FILE, [])[-100:])

    @app.route("/comunidad/send", methods=["POST"])
    def comunidad_send():
        u = usuario_actual()
        if not u:
            return jsonify({"error": "sin perfil"}), 401
        data = request.get_json(silent=True) or {}
        texto = str(data.get("text", "")).strip()[:300]
        if not texto:
            return jsonify({"error": "vacio"}), 400
        msgs = _leer(COMUNIDAD_FILE, [])
        msgs.append({"ff_id": u["ff_id"], "name": u["nombre"], "text": texto,
                     "time": datetime.now().strftime("%d/%m %H:%M")})
        _guardar(COMUNIDAD_FILE, msgs[-300:])
        return jsonify({"ok": True})

    # ----- 4) Perfil / registro (solo nombre + ID Free Fire) -----
    @app.route("/perfil", methods=["GET", "POST"])
    def perfil():
        error = ""
        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()[:20]
            ff_id = re.sub(r"\s", "", request.form.get("ff_id", ""))
            if len(nombre) < 2:
                error = "Escribe tu nombre (mínimo 2 letras)."
            elif not re.fullmatch(r"\d{5,15}", ff_id):
                error = "El ID de Free Fire solo lleva números."
            else:
                usuarios = cargar_usuarios()
                existente = next((x for x in usuarios if x["ff_id"] == ff_id), None)
                if existente:
                    if existente["nombre"].lower() == nombre.lower():
                        session.permanent = True
                        session["uid"] = ff_id
                        return redirect("/perfil")
                    error = "Ese ID ya está registrado con otro nombre."
                else:
                    usuarios.append({"ff_id": ff_id, "nombre": nombre, "fecha": datetime.now().strftime("%d/%m/%Y")})
                    guardar_usuarios(usuarios)
                    session.permanent = True
                    session["uid"] = ff_id
                    return redirect("/perfil")
        u = usuario_actual()
        miembros = "<h3 style='color:#a855f7'>👥 Comunidad</h3>" + _miembros_html()
        if u:
            cont = "<h2>👤 Mi perfil</h2>" + _tarjeta_perfil(u, True) + miembros
        else:
            err = "<div style='color:#ff6666;margin:8px 0'>%s</div>" % escape(error) if error else ""
            form = ("<div class='card'><h3 style='color:#a855f7;margin-top:0'>👤 Crear mi perfil</h3>"
                    "<small style='opacity:.7'>Solo tu nombre y tu ID de Free Fire. Sin correo.</small>%s"
                    "<form method='post'><input name='nombre' placeholder='Tu nombre' maxlength='20' required>"
                    "<input name='ff_id' placeholder='Tu ID de Free Fire' inputmode='numeric' required>"
                    "<button class='btn btn-p' style='width:100%%;margin:8px 0 0'>Entrar / Registrarme</button>"
                    "</form></div>") % err
            cont = "<h2>👤 Perfil</h2>" + form + miembros
        return pagina(cont, "perfil")

    @app.route("/perfil/salir")
    def perfil_salir():
        session.pop("uid", None)
        return redirect("/perfil")

    @app.route("/perfil/<ff_id>")
    def perfil_ver(ff_id):
        u = next((x for x in cargar_usuarios() if x["ff_id"] == ff_id), None)
        if not u:
            return pagina("<div class='card' style='text-align:center'>Ese perfil no existe.</div>", "perfil")
        propio = session.get("uid") == ff_id
        return pagina("<h2>👤 Perfil</h2>" + _tarjeta_perfil(u, propio), "perfil")

    # ----- Buscador -----
    @app.route("/buscar")
    def buscar():
        q = request.args.get("q", "").strip()
        ql = q.lower()

        def coincide(*campos):
            return any(ql in str(c or "").lower() for c in campos)

        res_v, res_e, res_d, res_u = [], [], [], []
        if ql:
            for v in cargar_videos():
                if coincide(v.get("titulo"), v.get("descripcion")):
                    href = v.get("link") or ("/uploads/videos/" + v["file"] if v.get("file") else "/videos")
                    res_v.append(("<a href='%s' target='_blank' style='text-decoration:none;color:white'>"
                                  "<div class='card' style='margin:6px 0;padding:12px'>🎬 <b>%s</b><br>"
                                  "<small style='opacity:.6'>%s</small></div></a>") % (
                        escape(href), escape(str(v.get("titulo", ""))), escape(str(v.get("descripcion", "")))))
            for e in cargar_eventos():
                if coincide(e.get("titulo"), e.get("lugar"), e.get("descripcion"), e.get("fecha")):
                    res_e.append(("<a href='/inscribir' style='text-decoration:none;color:white'>"
                                  "<div class='card' style='margin:6px 0;padding:12px'>📅 <b>%s</b> - %s<br>"
                                  "<small style='opacity:.6'>%s</small></div></a>") % (
                        escape(str(e.get("titulo", ""))), escape(str(e.get("fecha", ""))), escape(str(e.get("lugar", "")))))
            for d in cargar_duos():
                if coincide(d.get("duo"), d.get("id1"), d.get("id2")):
                    res_d.append(("<a href='/inscribir' style='text-decoration:none;color:white'>"
                                  "<div class='card' style='margin:6px 0;padding:12px'>🏆 <b>%s</b><br>"
                                  "<small style='opacity:.6'>%s + %s</small></div></a>") % (
                        escape(str(d.get("duo", ""))), escape(str(d.get("id1", ""))), escape(str(d.get("id2", "")))))
            for u in cargar_usuarios():
                if coincide(u.get("nombre"), u.get("ff_id")):
                    res_u.append(("<a href='/perfil/%s' style='text-decoration:none;color:white'>"
                                  "<div class='card' style='margin:6px 0;padding:12px'>👤 <b>%s</b><br>"
                                  "<small style='opacity:.6'>ID: %s</small></div></a>") % (
                        escape(u["ff_id"]), escape(u["nombre"]), escape(u["ff_id"])))
        if not ql:
            cuerpo = "<small style='opacity:.6'>Busca reels, eventos, dúos o jugadores por nombre o ID.</small>"
        else:
            cuerpo = (_seccion("🎬 Reels", res_v) + _seccion("📅 Eventos", res_e) +
                      _seccion("🏆 Dúos", res_d) + _seccion("👤 Jugadores", res_u))
            if not cuerpo:
                cuerpo = "<div class='card' style='text-align:center'>No encontré nada con «%s».</div>" % escape(q)
        cont = ("<h2>🔍 Buscar</h2><form method='get' action='/buscar'>"
                "<input name='q' value='%s' placeholder='Buscar reels, eventos, dúos, jugadores...' autofocus></form>%s") % (
            escape(q), cuerpo)
        return pagina(cont, "")


# ---------- activación automática (no hay que editar app.py) ----------
def activar(modulo):
    """Recibe el módulo app.py, registra las rutas nuevas y pone la barra en TODAS las páginas HTML."""
    app = modulo.app
    init_nav(app, modulo.estilos, modulo.widget_bot, modulo.cargar_videos, modulo.cargar,
             modulo.cargar_duos, modulo.es_admin, getattr(modulo, "MAX_DUOS", 12))

    @app.after_request
    def poner_barra(resp):
        try:
            if (resp.status_code == 200 and resp.mimetype == "text/html"
                    and not resp.direct_passthrough):
                html = resp.get_data(as_text=True)
                if "class='nav'" not in html:
                    activo = "reels" if request.path.startswith("/videos") else ""
                    resp.set_data(html + barra_nav(activo))
        except Exception:
            pass
        return resp

    return app
