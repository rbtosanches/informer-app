// Main JavaScript file for Informer application

/**
 * Show success message
 */
function showSuccess(message) {
    showAlert(message, 'success');
}

/**
 * Show error message
 */
function showError(message) {
    showAlert(message, 'danger');
}

/**
 * Show info message
 */
function showInfo(message) {
    showAlert(message, 'info');
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    // Insert alert at the top of the main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.insertAdjacentHTML('afterbegin', alertHtml);
    }
}

/**
 * Confirm before delete
 */
function confirmDelete(elementId) {
    return confirm('Tem certeza que deseja deletar este elemento?');
}

/**
 * Format date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
}

/**
 * Initialize tooltips
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

/**
 * Handle form submission with loading state
 */
function handleFormSubmit(formId, buttonId) {
    const form = document.getElementById(formId);
    const button = document.getElementById(buttonId);
    
    if (form && button) {
        form.addEventListener('submit', function() {
            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processando...';
        });
    }
}
