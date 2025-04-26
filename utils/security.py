# utils/security.py - Utilitaires de sécurité pour l'application NetSecurePro
# Ce fichier contient des fonctions utilitaires liées à la sécurité

import re
import hashlib
import secrets
import logging
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Configuration du logger
logger = logging.getLogger(__name__)


def is_strong_password(password):
    """
    Vérifie si un mot de passe est suffisamment fort.
    
    Critères:
    - Au moins 8 caractères
    - Au moins une lettre majuscule
    - Au moins une lettre minuscule
    - Au moins un chiffre
    - Au moins un caractère spécial
    
    Args:
        password (str): Le mot de passe à vérifier
        
    Returns:
        bool: True si le mot de passe est fort, False sinon
    """
    if len(password) < 8:
        return False
    
    # Vérifier la présence d'au moins une lettre majuscule
    if not re.search(r'[A-Z]', password):
        return False
    
    # Vérifier la présence d'au moins une lettre minuscule
    if not re.search(r'[a-z]', password):
        return False
    
    # Vérifier la présence d'au moins un chiffre
    if not re.search(r'\d', password):
        return False
    
    # Vérifier la présence d'au moins un caractère spécial
    if not re.search(r'[^A-Za-z0-9]', password):
        return False
    
    return True


def sanitize_input(text):
    """
    Sanitize user input to prevent XSS attacks.
    
    Args:
        text (str): The input text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Replace potentially dangerous characters
    sanitized = text.replace("<", "&lt;").replace(">", "&gt;")
    sanitized = sanitized.replace("\"", "&quot;").replace("'", "&#x27;")
    
    return sanitized


def generate_token():
    """
    Génère un token cryptographiquement sécurisé.
    
    Returns:
        str: Token généré
    """
    return secrets.token_hex(32)


def hash_data(data):
    """
    Hache des données avec SHA-256.
    
    Args:
        data (str): Les données à hacher
        
    Returns:
        str: Le hachage des données
    """
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def log_security_event(event_type, description, user_id=None, ip_address=None):
    """
    Journalise un événement de sécurité.
    
    Args:
        event_type (str): Type d'événement (login, logout, failed_login, etc.)
        description (str): Description de l'événement
        user_id (int, optional): ID de l'utilisateur concerné
        ip_address (str, optional): Adresse IP de l'utilisateur
    """
    logger.info(
        f"Security event: {event_type} | "
        f"User ID: {user_id or 'N/A'} | "
        f"IP: {ip_address or 'N/A'} | "
        f"Description: {description} | "
        f"Timestamp: {datetime.utcnow()}"
    )


def validate_email(email):
    """
    Valide une adresse email à l'aide d'une expression régulière.
    
    Args:
        email (str): L'adresse email à valider
        
    Returns:
        bool: True si l'email est valide, False sinon
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def secure_compare(a, b):
    """
    Compare deux chaînes de caractères de manière sécurisée (temps constant).
    
    Args:
        a (str): Première chaîne
        b (str): Deuxième chaîne
        
    Returns:
        bool: True si les chaînes sont identiques, False sinon
    """
    return secrets.compare_digest(a, b)


def create_password_hash(password):
    """
    Crée un hachage sécurisé d'un mot de passe.
    Utilise werkzeug.security.generate_password_hash avec des paramètres par défaut.
    
    Args:
        password (str): Le mot de passe à hacher
        
    Returns:
        str: Le hachage du mot de passe
    """
    return generate_password_hash(password)


def verify_password(password_hash, password):
    """
    Vérifie si un mot de passe correspond à un hachage.
    
    Args:
        password_hash (str): Le hachage du mot de passe
        password (str): Le mot de passe à vérifier
        
    Returns:
        bool: True si le mot de passe correspond au hachage, False sinon
    """
    return check_password_hash(password_hash, password)
