(function() {
    'use strict';

    // ==========================================
    // DOM Ready
    // ==========================================
    document.addEventListener('DOMContentLoaded', function() {
        
        // Initialize tooltips
        initTooltips();
        
        // Initialize popovers
        initPopovers();
        
        // Handle active nav links
        setActiveNavLink();
        
        // Form enhancements
        enhanceForms();
        
        // Image lazy loading
        lazyLoadImages();
        
        // Smooth scroll for anchor links
        smoothScrollLinks();
        
        // Auto-resize textareas
        autoResizeTextareas();
    });

    // ==========================================
    // Initialize Bootstrap Tooltips
    // ==========================================
    function initTooltips() {
        const tooltipTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // ==========================================
    // Initialize Bootstrap Popovers
    // ==========================================
    function initPopovers() {
        const popoverTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="popover"]')
        );
        popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    // ==========================================
    // Set Active Navigation Link
    // ==========================================
    function setActiveNavLink() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(function(link) {
            const href = link.getAttribute('href');
            if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
                link.classList.add('active');
            }
        });
    }

    // ==========================================
    // Form Enhancements
    // ==========================================
    function enhanceForms() {
        // Add loading state to submit buttons
        const forms = document.querySelectorAll('form');
        forms.forEach(function(form) {
            form.addEventListener('submit', function(e) {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn && !submitBtn.hasAttribute('data-allow-multiple')) {
                    // Prevent double submission
                    if (submitBtn.disabled) {
                        e.preventDefault();
                        return false;
                    }
                    
                    submitBtn.disabled = true;
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
                    
                    // Re-enable after 5 seconds as fallback
                    setTimeout(function() {
                        submitBtn.disabled = false;
                        submitBtn.innerHTML = originalText;
                    }, 5000);
                }
            });
        });

        // Bootstrap validation
        const validationForms = document.querySelectorAll('.needs-validation');
        validationForms.forEach(function(form) {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }

    // ==========================================
    // Lazy Load Images
    // ==========================================
    function lazyLoadImages() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver(function(entries, observer) {
                entries.forEach(function(entry) {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            const lazyImages = document.querySelectorAll('img.lazy');
            lazyImages.forEach(function(img) {
                imageObserver.observe(img);
            });
        }
    }

    // ==========================================
    // Smooth Scroll for Anchor Links
    // ==========================================
    function smoothScrollLinks() {
        const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
        smoothScrollLinks.forEach(function(link) {
            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href !== '#' && href !== '#!') {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        target.scrollIntoView({
                            // ==========================================
// Smooth Scroll for Anchor Links (Lanjutan)
// ==========================================
                        behavior: 'smooth'
                        });
                    }
                }
            });
        });
    }

    // ==========================================
    // Auto-Resize Textareas
    // ==========================================
    function autoResizeTextareas() {
        const textareas = document.querySelectorAll('textarea[data-auto-resize]');
        
        const resize = function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        };

        textareas.forEach(function(textarea) {
            // Initial resize
            resize.call(textarea);
            
            // Event listeners
            textarea.addEventListener('input', resize);
            textarea.addEventListener('change', resize);
            
            // Ensure resize happens on window load/resize for pre-filled forms
            window.addEventListener('load', resize.bind(textarea));
        });
    }

})(); // Penutup Self-Executing Function