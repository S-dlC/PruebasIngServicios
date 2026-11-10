from app import create_app
import os

modo = os.getenv("DEPLOYMENT_MODE", "production")
app = create_app(modo)