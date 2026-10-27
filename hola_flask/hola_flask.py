from flask import Flask # type: ignore
app = Flask(__name__)

@app.route('/')
def hola_flask():
    return '<em>¡Hola Flask!</em>'