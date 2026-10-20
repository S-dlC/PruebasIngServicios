from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Importamos el diccionario de configuraciones (production, development)
from config import app_config

# Crear el objeto db que servirá para conectar con la base de datos
db = SQLAlchemy()

# La factoría recibe como parámetro que configuración queremos usar
def create_app(config_name):
    # La app simplemente es una instancia de la clase Flask
    # La "receta" obliga a pasarle el nombre del módulo en que fue creada
    # que python guarda en la variable __name__. El parámetro
    # instance_relative_config es para decirle que cuando leamos
    # ficheros de configuración, lo haga de la carpeta ./instance
    app = Flask(__name__, instance_relative_config=True)

    # Una vez creada, la app debe almacenar una configuración
    # La sacamos del diccionario de configuraciones
    app.config.from_object(app_config[config_name])

    # Extendemos esa configuración con la URL de la base de datos
    # que leemos de otro fichero de configuración en ./instance
    app.config.from_pyfile('config.py')

    # Pasamos la aplicación ya configurada a db.init(), quien usará
    # la URL para conectar con la base de datos sql
    db.init_app(app)

    # Configuremos una ruta de prueba para la app
    @app.route("/")
    def prueba():
        return "¡Hola Flask con MariaDB!"

    return app