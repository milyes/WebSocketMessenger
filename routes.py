# routes.py - Définition des routes de l'application Flask NetSecurePro
# Ce fichier contient toutes les routes et vues de l'application

import logging
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from models import User, SecurityAlert, SecurityLog
from werkzeug.security import generate_password_hash, check_password_hash

# Configuration du logger pour ce module
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Route pour la page d'accueil"""
    logger.debug("Accès à la page d'accueil")
    return render_template('index.html', title="Accueil - NetSecurePro")


@app.route('/about')
def about():
    """Route pour la page à propos"""
    logger.debug("Accès à la page à propos")
    return render_template('about.html', title="À propos - NetSecurePro")


@app.route('/services')
def services():
    """Route pour la page des services"""
    logger.debug("Accès à la page des services")
    return render_template('services.html', title="Services - NetSecurePro")


@app.route('/contact')
def contact():
    """Route pour la page de contact"""
    logger.debug("Accès à la page de contact")
    return render_template('contact.html', title="Contact - NetSecurePro")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Route pour la page de connexion"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        logger.debug(f"Tentative de connexion pour l'utilisateur: {username}")
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=True)
            flash('Connexion réussie!', 'success')
            logger.info(f"Connexion réussie pour l'utilisateur: {username}")
            
            # Redirection vers la page demandée si elle existe
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Identifiants invalides. Veuillez réessayer.', 'danger')
            logger.warning(f"Échec de connexion pour l'utilisateur: {username}")
    
    return render_template('auth/login.html', title="Connexion - NetSecurePro")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Route pour la page d'inscription"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        logger.debug(f"Tentative d'inscription pour l'utilisateur: {username}")
        
        # Vérifications de base
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'danger')
            return render_template('auth/register.html')
        
        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Cet utilisateur ou cette adresse email existe déjà.', 'danger')
            return render_template('auth/register.html')
        
        # Créer le nouvel utilisateur
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
            logger.info(f"Inscription réussie pour l'utilisateur: {username}")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erreur lors de l'inscription de l'utilisateur {username}: {str(e)}")
            flash('Une erreur est survenue lors de l\'inscription. Veuillez réessayer.', 'danger')
    
    return render_template('auth/register.html', title="Inscription - NetSecurePro")


@app.route('/logout')
def logout():
    """Route pour la déconnexion"""
    if current_user.is_authenticated:
        logger.info(f"Déconnexion de l'utilisateur: {current_user.username}")
        logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    """Gestionnaire pour les erreurs 404"""
    logger.warning(f"Page non trouvée: {request.path}")
    return render_template('404.html', title="Page non trouvée"), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Gestionnaire pour les erreurs 500"""
    logger.error(f"Erreur serveur interne: {str(e)}")
    return render_template('500.html', title="Erreur serveur"), 500


# Route pour le tableau de bord utilisateur (nécessite une authentification)
@app.route('/dashboard')
@login_required
def dashboard():
    """Route pour le tableau de bord utilisateur"""
    logger.debug(f"Accès au tableau de bord par l'utilisateur: {current_user.username}")
    
    # Récupérer les alertes de sécurité pour l'utilisateur
    alerts = SecurityAlert.query.filter_by(user_id=current_user.id).order_by(SecurityAlert.created_at.desc()).limit(5).all()
    
    # Récupérer les journaux de sécurité pour l'utilisateur
    logs = SecurityLog.query.filter_by(user_id=current_user.id).order_by(SecurityLog.timestamp.desc()).limit(10).all()
    
    return render_template(
        'dashboard.html',
        title=f"Tableau de bord - {current_user.username}",
        user=current_user,
        alerts=alerts,
        logs=logs
    )


# Route API pour obtenir des informations de base sur la sécurité (exemple)
@app.route('/api/security-status')
def security_status():
    """API pour obtenir le statut de sécurité actuel"""
    # Exemple de données de statut (dans une vraie application, ces données seraient dynamiques)
    status = {
        'firewall_status': 'active',
        'last_scan': '2023-07-15 14:30:00',
        'threats_detected': 0,
        'system_health': 'good'
    }
    return jsonify(status)


# Avant de mettre l'application en production, vous pouvez ajouter plus de routes
# pour les fonctionnalités supplémentaires liées à la cybersécurité
