/* =========================================================
   CineVision AI
   Premium UI Interactions
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    /* -----------------------------------------------------
       Initialize Lucide Icons
    ----------------------------------------------------- */

    if (window.lucide) {
        lucide.createIcons();
    }


    /* -----------------------------------------------------
       Navbar Blur on Scroll
    ----------------------------------------------------- */

    const header = document.querySelector("header");

    if (header) {

        const updateHeader = () => {

            if (window.scrollY > 20) {

                header.style.background = "rgba(7, 7, 13, 0.92)";
                header.style.backdropFilter = "blur(25px)";
                header.style.webkitBackdropFilter = "blur(25px)";
                header.style.borderBottom =
                    "1px solid rgba(255, 255, 255, 0.1)";

            } else {

                header.style.background = "rgba(7, 7, 13, 0.72)";
                header.style.backdropFilter = "blur(22px)";
                header.style.webkitBackdropFilter = "blur(22px)";
                header.style.borderBottom =
                    "1px solid transparent";

            }

        };

        updateHeader();

        window.addEventListener("scroll", updateHeader);

    }


    /* -----------------------------------------------------
       Glass Card 3D Hover Effect
    ----------------------------------------------------- */

    const card = document.querySelector(".glassCard");

    if (card && window.matchMedia("(pointer: fine)").matches) {

        card.addEventListener("mousemove", (event) => {

            const rect = card.getBoundingClientRect();

            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;

            const rotateY = ((x / rect.width) - 0.5) * 10;
            const rotateX = ((y / rect.height) - 0.5) * -10;

            card.style.transform = `
                perspective(1200px)
                rotateX(${rotateX}deg)
                rotateY(${rotateY}deg)
                translateY(-6px)
            `;

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform = `
                perspective(1200px)
                rotateY(-5deg)
                rotateX(3deg)
            `;

        });

    }


    /* -----------------------------------------------------
       Smooth Scroll for Anchor Links
    ----------------------------------------------------- */

    const anchorLinks = document.querySelectorAll(
        'a[href^="#"]'
    );

    anchorLinks.forEach((link) => {

        link.addEventListener("click", (event) => {

            const targetId = link.getAttribute("href");

            if (!targetId || targetId === "#") {
                return;
            }

            const target = document.querySelector(targetId);

            if (target) {

                event.preventDefault();

                target.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }

        });

    });


    /* -----------------------------------------------------
       Watch Demo Modal
    ----------------------------------------------------- */

    const demoButton = document.querySelector(".demo");
    const modal = document.querySelector(".modal");
    const closeModalButton = document.querySelector(".close-modal");
    const modalVideo = document.querySelector(".modal video");

    const openModal = () => {

        if (!modal) {
            return;
        }

        modal.classList.add("active");
        modal.setAttribute("aria-hidden", "false");
        document.body.style.overflow = "hidden";

        if (modalVideo) {

            modalVideo.currentTime = 0;

            const playPromise = modalVideo.play();

            if (playPromise !== undefined) {

                playPromise.catch(() => {
                    // Browser may block autoplay.
                });

            }

        }

    };

    const closeModal = () => {

        if (!modal) {
            return;
        }

        modal.classList.remove("active");
        modal.setAttribute("aria-hidden", "true");
        document.body.style.overflow = "";

        if (modalVideo) {
            modalVideo.pause();
        }

    };

    if (demoButton) {
        demoButton.addEventListener("click", openModal);
    }

    if (closeModalButton) {
        closeModalButton.addEventListener("click", closeModal);
    }

    if (modal) {

        modal.addEventListener("click", (event) => {

            if (event.target === modal) {
                closeModal();
            }

        });

    }

    document.addEventListener("keydown", (event) => {

        if (event.key === "Escape") {
            closeModal();
        }

    });


    /* -----------------------------------------------------
       Form Loading State
    ----------------------------------------------------- */

    const storyForm = document.querySelector(".storyForm");

    if (storyForm) {

        storyForm.addEventListener("submit", () => {

            const submitButton =
                storyForm.querySelector('button[type="submit"]');

            if (!submitButton) {
                return;
            }

            submitButton.disabled = true;

            submitButton.innerHTML = `
                <span class="loading-spinner"></span>
                Creating Storyboard...
            `;

        });

    }


    /* -----------------------------------------------------
       Textarea Character Counter
    ----------------------------------------------------- */

    const storyTextarea = document.querySelector(
        'textarea[name="story"]'
    );

    if (storyTextarea) {

        const counter = document.createElement("small");

        counter.className = "character-counter";

        counter.style.display = "block";
        counter.style.marginTop = "8px";
        counter.style.color = "#77778d";
        counter.style.fontSize = "0.75rem";
        counter.textContent = "0 characters";

        storyTextarea.insertAdjacentElement(
            "afterend",
            counter
        );

        const updateCounter = () => {

            const count = storyTextarea.value.length;

            counter.textContent = `${count} characters`;

        };

        storyTextarea.addEventListener(
            "input",
            updateCounter
        );

        updateCounter();

    }


    /* -----------------------------------------------------
       Add Active Navigation Link
    ----------------------------------------------------- */

    const currentPath = window.location.pathname;

    const navigationLinks = document.querySelectorAll(
        "header nav ul a"
    );

    navigationLinks.forEach((link) => {

        const linkPath = link.pathname;

        if (
            linkPath === currentPath &&
            linkPath !== "/"
        ) {

            link.style.color = "#ffffff";

        }

    });


    /* -----------------------------------------------------
       Reveal Elements on Scroll
    ----------------------------------------------------- */

    const revealElements = document.querySelectorAll(
        ".feature-card, .scene-card, .summary-card, .story-result-card"
    );

    if ("IntersectionObserver" in window) {

        const observer = new IntersectionObserver(
            (entries, observerInstance) => {

                entries.forEach((entry) => {

                    if (entry.isIntersecting) {

                        entry.target.style.opacity = "1";
                        entry.target.style.transform =
                            "translateY(0)";

                        observerInstance.unobserve(
                            entry.target
                        );

                    }

                });

            },
            {
                threshold: 0.12
            }
        );

        revealElements.forEach((element) => {

            element.style.opacity = "0";
            element.style.transform = "translateY(20px)";
            element.style.transition =
                "opacity 0.6s ease, transform 0.6s ease";

            observer.observe(element);

        });

    }


    /* -----------------------------------------------------
       Video Fallback
    ----------------------------------------------------- */

    const videos = document.querySelectorAll("video");

    videos.forEach((video) => {

        video.addEventListener("error", () => {

            const videoSection =
                video.closest(".video-section");

            if (videoSection) {

                videoSection.style.background =
                    "linear-gradient(135deg, #281b38, #11111c)";

                video.style.display = "none";

            }

        });

    });


    /* -----------------------------------------------------
       Add Loading Spinner Style
    ----------------------------------------------------- */

    if (!document.querySelector("#cinevision-js-styles")) {

        const style = document.createElement("style");

        style.id = "cinevision-js-styles";

        style.textContent = `
            .loading-spinner {
                display: inline-block;
                width: 16px;
                height: 16px;
                margin-right: 8px;
                border: 2px solid rgba(255,255,255,0.35);
                border-top-color: #ffffff;
                border-radius: 50%;
                animation: cinevisionSpin 0.8s linear infinite;
                vertical-align: middle;
            }

            @keyframes cinevisionSpin {
                from {
                    transform: rotate(0deg);
                }

                to {
                    transform: rotate(360deg);
                }
            }

            button:disabled {
                cursor: wait;
                opacity: 0.75;
            }
        `;

        document.head.appendChild(style);

    }


    /* -----------------------------------------------------
       Initialize Icons Again
       Needed for dynamically inserted icons
    ----------------------------------------------------- */

    if (window.lucide) {
        lucide.createIcons();
    }

});