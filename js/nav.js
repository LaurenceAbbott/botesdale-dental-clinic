/* =============================================================================
   nav.js — site header behaviour
   • adds .is-scrolled to the header once the hero has passed
   • opens / closes the full-screen mobile menu (focus trapped, ESC to close)
   • expands the Treatments / Implant clinic groups inside the mobile menu
   ========================================================================== */
(function () {
  'use strict';

  var nav   = document.querySelector('[data-nav-root]');
  var menu  = document.getElementById('mobileMenu');
  var open  = document.getElementById('menuOpen');
  var close = document.getElementById('menuClose');

  /* --- scrolled state ----------------------------------------------------- */
  if (nav) {
    var hero = document.querySelector('.hero, .page-head');
    var threshold = hero ? hero.offsetHeight - 80 : 40;

    var onScroll = function () {
      nav.classList.toggle('is-scrolled', window.scrollY > threshold);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () {
      threshold = hero ? hero.offsetHeight - 80 : 40;
      onScroll();
    });
    onScroll();
  }

  /* --- mobile menu -------------------------------------------------------- */
  var lastFocus = null;

  function openMenu() {
    if (!menu) return;
    lastFocus = document.activeElement;
    menu.classList.add('is-open');
    document.body.classList.add('is-locked');
    if (open) open.setAttribute('aria-expanded', 'true');
    var first = menu.querySelector('a, button');
    if (first) first.focus();
  }

  function closeMenu() {
    if (!menu) return;
    menu.classList.remove('is-open');
    document.body.classList.remove('is-locked');
    if (open) open.setAttribute('aria-expanded', 'false');
    if (lastFocus) lastFocus.focus();
  }

  if (open)  open.addEventListener('click', openMenu);
  if (close) close.addEventListener('click', closeMenu);

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu && menu.classList.contains('is-open')) closeMenu();
  });

  /* Keep tabbing inside the sheet while it is open */
  if (menu) {
    menu.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab') return;
      var items = menu.querySelectorAll('a[href], button:not([disabled])');
      if (!items.length) return;
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  /* --- mobile submenu groups ---------------------------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll('.menu__toggle'), function (btn) {
    btn.addEventListener('click', function () {
      var sub = document.getElementById(btn.getAttribute('aria-controls'));
      if (!sub) return;
      var isOpen = sub.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(isOpen));
    });
  });

  /* Open the group that contains the current page */
  var activeSub = document.querySelector('.menu__sub a.is-active');
  if (activeSub) {
    var group = activeSub.closest('.menu__sub');
    var toggle = document.querySelector('[aria-controls="' + group.id + '"]');
    group.classList.add('is-open');
    if (toggle) toggle.setAttribute('aria-expanded', 'true');
  }
}());
