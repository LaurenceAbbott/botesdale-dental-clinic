/* =============================================================================
   main.js — small site-wide odds and ends.
   Loaded last; nav.js / ui.js / forms.js each stand alone.
   ========================================================================== */
(function () {
  'use strict';

  /* Current year in the footer */
  Array.prototype.forEach.call(document.querySelectorAll('[data-year]'), function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  /* Flag JS availability for progressive enhancement hooks in CSS */
  document.documentElement.classList.remove('no-js');
  document.documentElement.classList.add('js');
}());
