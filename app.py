from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>LIGA LOS TOXICOS</h1>
    <p>App creada gratis y funcionando!</p>
    <p>Proximamente: tabla de posiciones</p>
    <style>
      body { font-family: sans-serif; text-align: center; margin-top: 50px; background: #111; color: white; }
      h1 { color: #00ff88; }
    </style>
    """
