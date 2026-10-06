from flask import Flask
app = Flask(__name__)

@app.route('/')
def hola_flask():
    return '<em>¡Hola Flask!</em>'