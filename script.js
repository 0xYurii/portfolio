// Portfolio JavaScript
document.addEventListener("DOMContentLoaded", function() {
    // Theme toggle functionality
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;
    
    // Check for saved theme preference or default to light mode
    const currentTheme = localStorage.getItem("theme") || "light";
    body.setAttribute("data-theme", currentTheme);
    updateThemeIcon(currentTheme);
    
    // Theme toggle event listener
    if (themeToggle) {
        themeToggle.addEventListener("click", function(e) {
            e.preventDefault();
            
            const currentTheme = body.getAttribute("data-theme");
            
            const newTheme = currentTheme === "light" ? "dark" : "light";
            
            
            body.setAttribute("data-theme", newTheme);
            localStorage.setItem("theme", newTheme);
            updateThemeIcon(newTheme);
            
        });
    } else {
        
    }
    
    // Update theme icon based on current theme
    function updateThemeIcon(theme) {
        if (themeToggle) {
            const icon = themeToggle.querySelector("i");
            if (icon) {
                if (theme === "dark") {
                    icon.className = "fas fa-sun";
                } else {
                    icon.className = "fas fa-moon";
                }
            }
        }
    }
    
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const targetId = this.getAttribute("href");
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerHeight = document.querySelector(".header").offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: "smooth"
                });
            }
        });
    });
    
    // Mobile menu toggle (hamburger menu)
    const hamburger = document.getElementById("hamburger");
    const navLinksContainer = document.querySelector(".nav-links");
    
    if (hamburger && navLinksContainer) {
        hamburger.addEventListener("click", function() {
            navLinksContainer.classList.toggle("active");
            hamburger.classList.toggle("active");
        });
    }
    
    // Animate skill bars when they come into view
    const skillBars = document.querySelectorAll(".skill-bar");
    const observerOptions = {
        threshold: 0.5,
        rootMargin: "0px 0px -100px 0px"
    };
    
    const skillBarObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("animate");
            }
        });
    }, observerOptions);
    
    skillBars.forEach(bar => {
        skillBarObserver.observe(bar);
    });

    // Animate progress bars when they come into view
    const progressBars = document.querySelectorAll('.progress-bar');
    const progressObserverOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const progressObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Reset width to 0 for animation
                entry.target.style.width = '0%';
                // Animate to full width
                setTimeout(() => {
                    if (entry.target.classList.contains('beginner')) {
                        entry.target.style.width = '50%';
                    } else if (entry.target.classList.contains('intermediate')) {
                        entry.target.style.width = '75%';
                    } else if (entry.target.classList.contains('advanced')) {
                        entry.target.style.width = '100%';
                    }
                }, 200);
            }
        });
    }, progressObserverOptions);
    
    progressBars.forEach(bar => {
        progressObserver.observe(bar);
    });
    
    // Add scroll effect to header
    let lastScrollTop = 0;
    const header = document.querySelector(".header");
    
    window.addEventListener("scroll", function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            header.style.transform = "translateY(-100%)";
        } else {
            // Scrolling up
            header.style.transform = "translateY(0)";
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Add typing effect to hero title (disabled to prevent HTML parsing issues)
    // Typing animation is disabled to prevent HTML parsing issues
    // This section is commented out to avoid syntax errors
    
    // Add parallax effect to hero section
    const hero = document.querySelector(".hero");
    if (hero) {
        window.addEventListener("scroll", function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            hero.style.transform = `translateY(${rate}px)`;
        });
    }
    
    // Add hover effects to project cards
    const projectCards = document.querySelectorAll(".project-card");
    projectCards.forEach(card => {
        card.addEventListener("mouseenter", function() {
            this.style.transform = "translateY(-8px) scale(1.02)";
        });
        
        card.addEventListener("mouseleave", function() {
            this.style.transform = "translateY(0) scale(1)";
        });
    });
    
    // Add click effect to buttons
    const buttons = document.querySelectorAll(".btn");
    buttons.forEach(button => {
        button.addEventListener("click", function(e) {
            // Create ripple effect
            const ripple = document.createElement("span");
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + "px";
            ripple.style.left = x + "px";
            ripple.style.top = y + "px";
            ripple.classList.add("ripple");
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Add CSS for ripple effect
    const style = document.createElement("style");
    style.textContent = `
        .btn {
            position: relative;
            overflow: hidden;
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .nav-links.active {
            display: flex;
            flex-direction: column;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-top: none;
            padding: 1rem;
            box-shadow: var(--shadow-lg);
        }
        
        .hamburger.active span:nth-child(1) {
            transform: rotate(45deg) translate(5px, 5px);
        }
        
        .hamburger.active span:nth-child(2) {
            opacity: 0;
        }
        
        .hamburger.active span:nth-child(3) {
            transform: rotate(-45deg) translate(7px, -6px);
        }
        
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Console message for developers
    console.log("%c👋 Hello there!", "color: #3b82f6; font-size: 20px; font-weight: bold;");
    console.log("%cThanks for checking out the code! This portfolio was built with vanilla HTML, CSS, and JavaScript.", "color: #64748b; font-size: 14px;");
    console.log("%cFeel free to reach out if you have any questions or want to collaborate!", "color: #8b5cf6; font-size: 14px;");
});
