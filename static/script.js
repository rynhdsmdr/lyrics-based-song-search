// static/script.js

document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("search-form");
    const spinner = document.getElementById("spinner");
    const queryInput = document.getElementById("query");
    const resultsContainer = document.getElementById("results");
    const themeToggle = document.getElementById("theme-toggle");
    const backToTop = document.getElementById("back-to-top");

    // Show spinner on submit
    if (form) {
        form.addEventListener("submit", function(e) {
            spinner.classList.remove("hidden");
        });
    }

    // Theme toggle: saves to localStorage
    const applyTheme = (dark) => {
        if (dark) document.body.classList.add("dark");
        else document.body.classList.remove("dark");
    };
    const saved = localStorage.getItem("dark_mode");
    applyTheme(saved === "1");
    if (themeToggle) {
        themeToggle.addEventListener("click", function() {
            const isDark = document.body.classList.toggle("dark");
            localStorage.setItem("dark_mode", isDark ? "1":"0");
        });
    }

    // Smooth scroll for back-to-top
    if (backToTop) {
        backToTop.addEventListener("click", function(e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Highlight query in .snippet elements
    function highlightQuery(q) {
        if (!q) return;
        // escape special regex characters
        const esc = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        // create regex to highlight full query and fallback single words
        const regexAll = new RegExp(esc, 'ig');

        const snippets = document.querySelectorAll('.snippet');
        snippets.forEach(el => {
            let text = el.getAttribute('data-raw') || el.textContent;
            // first try full query
            if (regexAll.test(text)) {
                text = text.replace(regexAll, m => `<mark>${m}</mark>`);
            } else {
                // highlight any token
                q.split(/\s+/).forEach(tok => {
                    if (tok.length < 2) return;
                    const re = new RegExp(tok.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'ig');
                    text = text.replace(re, m => `<mark>${m}</mark>`);
                });
            }
            el.innerHTML = text;
        });
    }

    // init highlight with query from input (if present)
    if (queryInput && queryInput.value) {
        highlightQuery(queryInput.value.trim());
        // scroll to results smoothly
        if (resultsContainer) {
            setTimeout(() => resultsContainer.scrollIntoView({behavior: 'smooth', block: 'start'}), 200);
        }
    }

    // hide spinner after page load (in case)
    spinner.classList.add("hidden");
});
