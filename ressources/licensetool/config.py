import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# Lädt .env-Datei automatisch
load_dotenv(os.path.join(basedir, '..', '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OIDC-Konfiguration aus .env
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    TENANT_ID = os.environ.get('TENANT_ID')
