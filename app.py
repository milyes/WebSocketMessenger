# app.py - Configuration de l'application Flask pour NetSecurePro
# Ce fichier contient la configuration principale de l'application Flask

import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix


# Configuration du logging pour faciliter le débogage
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Initialisation de l'application Flask NetSecurePro")


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# Création de l'application Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Configuration du middleware ProxyFix pour générer les URLs avec HTTPS
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration de la base de données
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///netsecurepro.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialisation des extensions avec l'application
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Création des tables dans la base de données
with app.app_context():
    # Import des modèles (doit être fait ici pour que les tables soient créées)
    import models  # noqa: F401
    
    logger.info("Création des tables dans la base de données")
    db.create_all()
    logger.info("Tables créées avec succès")

logger.info("Application Flask NetSecurePro initialisée avec succès")
