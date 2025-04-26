/**
 * main.js - JavaScript principal pour l'application NetSecurePro
 * Ce fichier contient les fonctions JavaScript utilisées dans l'application
 */

// Attendre que le DOM soit complètement chargé
document.addEventListener('DOMContentLoaded', function() {
    console.log('NetSecurePro application JavaScript initialized');
    initializeTooltips();
    setupSecurityCardAnimations();
    setupFormValidation();
});

/**
 * Initialise les tooltips Bootstrap
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Configure les animations pour les cartes de sécurité
 */
function setupSecurityCardAnimations() {
    const securityCards = document.querySelectorAll('.security-card');
    
    securityCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow-lg');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-lg');
        });
    });
}

/**
 * Configure la validation des formulaires
 */
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Affiche une notification à l'utilisateur
 * @param {string} message - Le message à afficher
 * @param {string} type - Le type de notification (success, warning, danger, info)
 */
function showNotification(message, type = 'info') {
    const alertPlaceholder = document.getElementById('alert-placeholder');
    if (!alertPlaceholder) return;
    
    const wrapper = document.createElement('div');
    wrapper.classList.add('alert', `alert-${type}`, 'alert-dismissible', 'fade', 'show');
    wrapper.setAttribute('role', 'alert');
    
    wrapper.innerHTML = `
        <div>${message}</div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertPlaceholder.append(wrapper);
    
    // Auto-dismiss après 5 secondes
    setTimeout(() => {
        const alert = bootstrap.Alert.getOrCreateInstance(wrapper);
        alert.close();
    }, 5000);
}

/**
 * Fonction simulée pour vérifier le statut de sécurité
 * Dans une vraie application, cela ferait un appel API
 */
function checkSecurityStatus() {
    fetch('/api/security-status')
        .then(response => response.json())
        .then(data => {
            updateSecurityDashboard(data);
        })
        .catch(error => {
            console.error('Erreur lors de la récupération du statut de sécurité:', error);
        });
}

/**
 * Met à jour le tableau de bord de sécurité avec les données récupérées
 * @param {Object} data - Les données de sécurité
 */
function updateSecurityDashboard(data) {
    const statusElement = document.getElementById('security-status');
    if (!statusElement) return;
    
    const firewallStatus = document.getElementById('firewall-status');
    const lastScan = document.getElementById('last-scan');
    const threatsDetected = document.getElementById('threats-detected');
    const systemHealth = document.getElementById('system-health');
    
    if (firewallStatus) firewallStatus.textContent = data.firewall_status;
    if (lastScan) lastScan.textContent = data.last_scan;
    if (threatsDetected) threatsDetected.textContent = data.threats_detected;
    if (systemHealth) systemHealth.textContent = data.system_health;
    
    // Mettre à jour les classes en fonction du statut
    if (data.threats_detected > 0) {
        statusElement.className = 'security-status status-danger';
        statusElement.textContent = 'Menace détectée';
    } else if (data.firewall_status !== 'active') {
        statusElement.className = 'security-status status-warning';
        statusElement.textContent = 'Attention requise';
    } else {
        statusElement.className = 'security-status status-secure';
        statusElement.textContent = 'Sécurisé';
    }
}
