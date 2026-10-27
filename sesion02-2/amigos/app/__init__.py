from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import render_template

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

    # Pero ahora no implementamos aquí funciones ni rutas
    # eso lo hacen los blueprints. Aquí simplemente registramos
    # esos blueprints para "montarlos" en una ruta
    from .html import html as html_blueprint
    app.register_blueprint(html_blueprint, url_prefix='/html')
        
    migrate = Migrate(app, db)
    from app import models
    return app
