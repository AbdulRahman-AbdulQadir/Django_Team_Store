document.addEventListener('DOMContentLoaded', function () {
  const aside = document.querySelector('aside'); // selects your aside (assumes 1 aside)
  if (!aside) return;

  const LG_BREAKPOINT = 1024; // Tailwind 'lg' = 1024px
  const TOP_OFFSET_PX = 32;   // equivalent to lg:top-8 (2rem -> 32px)

  function updateSticky() {
    if (window.innerWidth >= LG_BREAKPOINT) {
      // apply sticky via JS (doesn't change your classes in HTML)
      aside.style.position = 'sticky';
      aside.style.top = TOP_OFFSET_PX + 'px';
      aside.style.zIndex = '10'; // optional so it stays above content
    } else {
      // remove inline styles on smaller screens
      aside.style.position = '';
      aside.style.top = '';
      aside.style.zIndex = '';
    }
  }

  updateSticky();
  window.addEventListener('resize', updateSticky);
});
