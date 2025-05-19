// Dashboard Interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations for elements with animate-on-scroll class
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    animateElements.forEach(element => {
        observer.observe(element);
    });

    // Handle refresh buttons
    document.querySelectorAll('.refresh-btn').forEach(button => {
        button.addEventListener('click', function() {
            const card = this.closest('.dashboard-card');
            this.classList.add('rotating');
            
            // Simulate refresh with animation
            setTimeout(() => {
                this.classList.remove('rotating');
            }, 1000);
        });
    });

    // Add hover effects to action buttons
    document.querySelectorAll('.action-button').forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.classList.add('hover-lift');
        });
        
        button.addEventListener('mouseleave', function() {
            this.classList.remove('hover-lift');
        });
    });

    // Add smooth scrolling to all internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize tooltips if any
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function(e) {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            tooltip.style.left = rect.left + (rect.width - tooltip.offsetWidth) / 2 + 'px';
            
            setTimeout(() => tooltip.classList.add('show'), 50);
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltips = document.querySelectorAll('.tooltip');
            tooltips.forEach(t => {
                t.classList.remove('show');
                setTimeout(() => t.remove(), 200);
            });
        });
    });

    // Add loading state to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = this.querySelector('[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                const originalText = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                
                // Reset button after 5 seconds if form hasn't redirected
                setTimeout(() => {
                    if (document.body.contains(submitButton)) {
                        submitButton.disabled = false;
                        submitButton.innerHTML = originalText;
                    }
                }, 5000);
            }
        });
    });
});
