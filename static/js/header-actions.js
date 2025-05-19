// Header Actions Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Support Modal Handling
    const supportModal = document.getElementById('support-modal');
    const modalBackdrop = document.querySelector('.modal-backdrop');
    const modalClose = document.querySelector('.modal-close');
    const supportAction = document.querySelector('.support-action');

    function openModal() {
        supportModal.classList.add('show');
        modalBackdrop.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        supportModal.classList.remove('show');
        modalBackdrop.classList.remove('show');
        document.body.style.overflow = '';
    }

    if (supportAction) {
        supportAction.addEventListener('click', function(e) {
            e.preventDefault();
            openModal();
        });
    }

    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }

    if (modalBackdrop) {
        modalBackdrop.addEventListener('click', closeModal);
    }

    // Close modal on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && supportModal.classList.contains('show')) {
            closeModal();
        }
    });

    // Emergency Action Handling
    const emergencyAction = document.querySelector('.emergency-action');
    if (emergencyAction) {
        emergencyAction.addEventListener('click', function(e) {
            // Add a confirmation for emergency calls
            if (!e.target.classList.contains('confirmed')) {
                e.preventDefault();
                if (confirm('This will redirect you to emergency contacts. Continue?')) {
                    window.location.href = this.href;
                }
            }
        });
    }

    // Add hover animation for action items
    const actionItems = document.querySelectorAll('.action-item');
    actionItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });

        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });

        item.addEventListener('click', function() {
            // Add click effect
            this.style.transform = 'translateY(1px)';
            setTimeout(() => {
                this.style.transform = 'translateY(0)';
            }, 100);
        });
    });
});
