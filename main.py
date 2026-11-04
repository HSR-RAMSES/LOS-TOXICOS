# Arranca la app con la barra estilo TikTok sin tocar app.py
import os
import app as mi_app          # tu app.py
from navbar import activar

app = activar(mi_app)         # (si usas gunicorn: main:app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
