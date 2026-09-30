document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("comic-form");
    const button = document.getElementById("generate-button");

    if (!form || !button) {
        return;
    }

    const idleLabel = button.textContent;

    form.addEventListener("submit", () => {
        button.disabled = true;
        button.textContent = "⏳ Generating Comic...";
    });

    // Coming back with the browser Back button restores the page from cache
    // with the button still disabled - reset it.
    window.addEventListener("pageshow", (event) => {
        if (event.persisted) {
            button.disabled = false;
            button.textContent = idleLabel;
        }
    });
});
