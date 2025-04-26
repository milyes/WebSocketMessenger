# main.py - Point d'entrée principal pour l'application Flask NetSecurePro
# Ce fichier importe l'application Flask depuis app.py et permet le démarrage du serveur

from app import app  # noqa: F401
import routes  # Importe les routes de l'application

# Ce fichier est configuré pour être l'entrée principale de l'application Flask
# Le serveur démarrera automatiquement lors de l'exécution de ce fichier
