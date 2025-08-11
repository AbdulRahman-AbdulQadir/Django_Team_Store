function dismissMessage(id) {
    const el = document.getElementById(id);
    // fade out...
    el.classList.add('fade-out');
    // then remove from DOM
    setTimeout(() => el.remove(), 300);
}