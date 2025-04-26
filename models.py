# models.py - Définition des modèles de données pour l'application NetSecurePro
# Ce fichier contient les classes qui représentent les tables dans la base de données

from app import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    """Modèle pour les utilisateurs de l'application"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    role = db.Column(db.String(20), default='user')  # 'user', 'admin', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'


class SecurityAlert(db.Model):
    """Modèle pour les alertes de sécurité"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # 'low', 'medium', 'high', 'critical'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    user = db.relationship('User', backref=db.backref('alerts', lazy=True))
    
    def __repr__(self):
        return f'<SecurityAlert {self.title}>'


class SecurityLog(db.Model):
    """Modèle pour les journaux de sécurité"""
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    user = db.relationship('User', backref=db.backref('logs', lazy=True))
    
    def __repr__(self):
        return f'<SecurityLog {self.event_type}>'
