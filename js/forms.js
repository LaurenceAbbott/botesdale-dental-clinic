/* =============================================================================
   forms.js — progressive client-side validation
   -----------------------------------------------------------------------------
   Every form marked [data-validate] is validated on submit and, once a field
   has been touched, on blur. Nothing is sent anywhere: on success the form is
   replaced by its success panel.

   >>> TO GO LIVE <<<
   Pick one of these and the rest of the file stays as it is:
     1. Formspree  — set action="https://formspree.io/f/XXXX" method="post"
                     on the <form> and delete the `e.preventDefault()` branch
                     inside handleSubmit (keep the validation call).
     2. Netlify    — add  netlify  and  name="..."  to the <form> element.
     3. Own endpoint — replace the SUCCESS block below with a fetch() POST.
   ========================================================================== */
(function () {
  'use strict';

  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var PHONE = /^[0-9\s()+.-]{7,}$/;

  function fieldOf(input) { return input.closest('.field') || input.closest('.fieldset'); }

  function messageFor(input) {
    var v = (input.value || '').trim();

    if (input.required && input.type !== 'checkbox' && !v) return 'This field is required.';
    if (input.required && input.type === 'checkbox' && !input.checked) return 'Please confirm to continue.';
    if (!v) return '';
    if (input.type === 'email' && !EMAIL.test(v)) return 'Enter a valid email address.';
    if (input.type === 'tel' && !PHONE.test(v)) return 'Enter a valid phone number.';
    if (input.minLength > 0 && v.length < input.minLength) return 'Please enter at least ' + input.minLength + ' characters.';
    return '';
  }

  function validateField(input) {
    var wrap = fieldOf(input);
    if (!wrap) return true;
    var msg = messageFor(input);
    var box = wrap.querySelector('.field__error');

    wrap.classList.toggle('has-error', !!msg);
    wrap.classList.toggle('is-valid', !msg && !!(input.value || '').trim());
    input.setAttribute('aria-invalid', msg ? 'true' : 'false');
    if (box) box.textContent = msg;
    return !msg;
  }

  Array.prototype.forEach.call(document.querySelectorAll('[data-validate]'), function (form) {
    var inputs = Array.prototype.slice.call(form.querySelectorAll('input, select, textarea'))
      .filter(function (el) { return el.type !== 'hidden' && el.type !== 'submit'; });

    inputs.forEach(function (input) {
      input.addEventListener('blur', function () {
        if (input.dataset.touched) validateField(input);
      });
      input.addEventListener('input', function () {
        input.dataset.touched = '1';
        var wrap = fieldOf(input);
        if (wrap && wrap.classList.contains('has-error')) validateField(input);
      });
      input.addEventListener('change', function () { input.dataset.touched = '1'; });
    });

    form.addEventListener('submit', function (e) {
      var firstBad = null;
      inputs.forEach(function (input) {
        input.dataset.touched = '1';
        if (!validateField(input) && !firstBad) firstBad = input;
      });

      if (firstBad) {
        e.preventDefault();
        firstBad.focus();
        firstBad.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }

      /* --- SUCCESS ---------------------------------------------------------
         Remove this block once a real endpoint is wired up (see header). */
      e.preventDefault();
      var success = document.getElementById(form.dataset.success);
      form.hidden = true;
      if (success) {
        success.hidden = false;
        success.setAttribute('tabindex', '-1');
        success.focus();
        success.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });
}());
