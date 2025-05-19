// Add smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add loading indicators
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        const submitButton = this.querySelector('[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner"></span> Processing...';
        }
    });
});

// Add fade-in animation for cards
const observerOptions = {
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.card').forEach(card => {
    card.classList.add('animate-on-scroll');
    observer.observe(card);
});

// Add dropdown menu interactions
document.querySelectorAll('.dropdown').forEach(dropdown => {
    const trigger = dropdown.querySelector('.dropbtn');
    const content = dropdown.querySelector('.dropdown-content');
    
    if (trigger && content) {
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            content.classList.toggle('show');
        });
    }
});

// Close dropdowns when clicking outside
document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-content').forEach(content => {
        content.classList.remove('show');
    });
});

// Add notification badge updates
function updateNotificationBadge() {
    fetch('/notifications/count/')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.notification-badge');
            if (badge && data.count > 0) {
                badge.textContent = data.count;
                badge.classList.add('active');
            }
        });
}

// Add responsive table handling
const tables = document.querySelectorAll('.table');
tables.forEach(table => {
    const headerCells = table.querySelectorAll('th');
    const rows = table.querySelectorAll('tbody tr');
    
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        cells.forEach((cell, index) => {
            cell.setAttribute('data-label', headerCells[index].textContent);
        });
    });
});

// Add form validation feedback
document.querySelectorAll('form').forEach(form => {
    const inputs = form.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        input.addEventListener('blur', () => {
            if (input.checkValidity()) {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
            } else {
                input.classList.remove('is-valid');
                input.classList.add('is-invalid');
            }
        });
    });
});
