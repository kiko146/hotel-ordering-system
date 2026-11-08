// Small progressive enhancement: prevent accidental repeated checkout clicks.
document.querySelectorAll('.checkout-form').forEach((form) => {
  form.addEventListener('submit', () => {
    const button = form.querySelector('button[type="submit"]');
    if (button) {
      button.disabled = true;
      button.textContent = 'Placing your order...';
    }
  });
});
