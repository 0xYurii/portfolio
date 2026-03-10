document.addEventListener("DOMContentLoaded", () => {
    const html = document.documentElement;
    const toggle = document.getElementById("theme-toggle");
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.getElementById("nav-links");
    const header = document.querySelector(".header");

    // ── Theme ──────────────────────────────────────────
    const saved = localStorage.getItem("theme");
    if (saved) {
        html.setAttribute("data-theme", saved);
    }
    syncIcon();

    toggle.addEventListener("click", () => {
        const next = html.getAttribute("data-theme") === "dark" ? "light" : "dark";
        html.setAttribute("data-theme", next);
        localStorage.setItem("theme", next);
        syncIcon();
    });

    function syncIcon() {
        const icon = toggle.querySelector("i");
        if (html.getAttribute("data-theme") === "dark") {
            icon.className = "fas fa-sun";
        } else {
            icon.className = "fas fa-moon";
        }
    }

    // ── Mobile menu ────────────────────────────────────
    hamburger.addEventListener("click", () => {
        hamburger.classList.toggle("active");
        navLinks.classList.toggle("active");
    });

    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", () => {
            hamburger.classList.remove("active");
            navLinks.classList.remove("active");
        });
    });

    // ── Header hide on scroll down ────────────────────
    let lastY = 0;
    window.addEventListener("scroll", () => {
        const y = window.scrollY;
        if (y > lastY && y > 80) {
            header.classList.add("hidden");
        } else {
            header.classList.remove("hidden");
        }
        lastY = y;
    }, { passive: true });

    // ── Smooth scroll for anchor links ────────────────
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener("click", e => {
            const target = document.querySelector(a.getAttribute("href"));
            if (!target) return;
            e.preventDefault();
            const top = target.offsetTop - header.offsetHeight - 8;
            window.scrollTo({ top, behavior: "smooth" });
        });
    });

    // ── Scroll-triggered animations ───────────────────
    const observer = new IntersectionObserver(
        entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                }
            });
        },
        { threshold: 0.08, rootMargin: "0px 0px -40px 0px" }
    );

    // hero elements
    [".hero-label", ".hero-title", ".hero-subtitle", ".hero-cta", ".hero-visual"]
        .forEach(sel => {
            const el = document.querySelector(sel);
            if (el) observer.observe(el);
        });

    // project cards with staggered delay
    document.querySelectorAll(".project-card").forEach((card, i) => {
        card.style.transitionDelay = `${i * 0.06}s`;
        observer.observe(card);
    });

    // skill groups with staggered delay
    document.querySelectorAll(".skill-group").forEach((group, i) => {
        group.style.transitionDelay = `${i * 0.08}s`;
        observer.observe(group);
    });

    // contact
    const contactText = document.querySelector(".contact-text");
    const contactTerminal = document.querySelector(".contact-terminal");
    if (contactText) observer.observe(contactText);
    if (contactTerminal) observer.observe(contactTerminal);

    // section headers
    document.querySelectorAll(".section-header").forEach(h => {
        h.classList.add("fade-up");
        observer.observe(h);
    });
});
