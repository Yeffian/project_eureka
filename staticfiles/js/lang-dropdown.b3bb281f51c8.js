(function () {
  const btn = document.getElementById('lang-btn');
  const menu = document.getElementById('lang-menu');
  const form = document.getElementById('lang-form');
  const input = document.getElementById('selected-lang');

  // Bail cleanly if the dropdown isn't on this page — avoids a null.addEventListener crash
  if (!btn || !menu || !form || !input) return;

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const wasHidden = menu.classList.contains('hidden');
    menu.classList.toggle('hidden');
    btn.setAttribute('aria-expanded', String(wasHidden));
  });

  document.addEventListener('click', () => {
    menu.classList.add('hidden');
    btn.setAttribute('aria-expanded', 'false');
  });

  document.querySelectorAll('.lang-opt').forEach((opt) => {
    opt.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      input.value = opt.getAttribute('data-lang');
      form.submit();
    });
  });
})();