# config.py - Configuration de l'application Flask NetSecurePro
# Ce fichier contient la configuration de l'application Flask

import os
from datetime import timedelta


class Config:
    """Configuration de base pour l'application Flask"""
    
    # Configuration générale
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'default_secret_key_for_development')
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']
    TESTING = False
    
    # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///netsecurepro.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Configuration de session
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Configuration de sécurité
    SESSION_COOKIE_SECURE = False  # Mettre à True en production avec HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Configuration des téléchargements de fichiers
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max pour les téléchargements
    
    # Configuration du logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')


class DevelopmentConfig(Config):
    """Configuration pour l'environnement de développement"""
    DEBUG = True
    

class TestingConfig(Config):
    """Configuration pour l'environnement de test"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    

class ProductionConfig(Config):
    """Configuration pour l'environnement de production"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    # En production, assurez-vous que la clé secrète est définie
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Vérifier que SECRET_KEY est défini
        assert os.environ.get('SESSION_SECRET'), "SESSION_SECRET doit être défini en production"
        
        # Autres configurations de production ici


# Dictionnaire des configurations disponibles
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Récupère la configuration en fonction de l'environnement"""
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])
