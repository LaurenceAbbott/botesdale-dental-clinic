/* =============================================================================
   ui.js — interactive components
   • sticky tab nav with scroll-spy
   • chooser (tab switcher — one panel per audience)
   • accordions
   • testimonial carousel (auto-advancing, pauses on hover/focus)
   • reveal-on-scroll
   • back-to-top
   • image lightbox
   • cookie banner
   ========================================================================== */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var behavior = reduceMotion ? 'auto' : 'smooth';

  /* --- 1. Sticky tab nav + scroll-spy ------------------------------------- */
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.tab'));
  if (tabs.length) {
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function (e) {
        e.preventDefault();
        tab.classList.add('is-pressed');
        setTimeout(function () { tab.classList.remove('is-pressed'); }, 100);
        var target = document.getElementById(tab.dataset.target);
        if (target) target.scrollIntoView({ behavior: behavior, block: 'start' });
      });
    });

    var spied = tabs
      .map(function (t) { return document.getElementById(t.dataset.target); })
      .filter(Boolean);

    if ('IntersectionObserver' in window && spied.length) {
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          tabs.forEach(function (t) {
            t.classList.toggle('is-active', t.dataset.target === entry.target.id);
          });
        });
      }, { rootMargin: '-40% 0px -55% 0px', threshold: 0 });
      spied.forEach(function (s) { spy.observe(s); });
    }
  }

  /* --- 1b. Chooser (tab switcher) -----------------------------------------
     Shows one panel at a time where a page carries one form per audience.
     The markup ships with the tab row hidden and every panel visible, so with
     JavaScript off both forms are still there — this only ever hides things
     once it can also offer a way to get them back. */
  Array.prototype.forEach.call(document.querySelectorAll('[data-chooser]'), function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute('aria-controls')); });
    if (tabs.length < 2 || panels.indexOf(null) !== -1) return;

    var tabRow = root.querySelector('[role="tablist"]');
    if (tabRow) tabRow.hidden = false;
    root.classList.add('is-enhanced');

    function select(i, opts) {
      opts = opts || {};
      tabs.forEach(function (tab, n) {
        var on = n === i;
        tab.setAttribute('aria-selected', on ? 'true' : 'false');
        /* Roving tabindex: one stop for the group, arrows move within it. */
        tab.tabIndex = on ? 0 : -1;
        panels[n].hidden = !on;
      });
      if (opts.focus) tabs[i].focus();
      /* Only a real choice touches the URL — writing on load would throw away
         whatever anchor the visitor actually arrived at. */
      if (opts.hash && history.replaceState) {
        history.replaceState(null, '', '#' + tabs[i].dataset.chooserKey);
      }
    }

    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { select(i, { hash: true }); });
      tab.addEventListener('keydown', function (e) {
        var to = e.key === 'ArrowRight' ? i + 1
               : e.key === 'ArrowLeft' ? i - 1
               : e.key === 'Home' ? 0
               : e.key === 'End' ? tabs.length - 1 : -1;
        if (to === -1) return;
        e.preventDefault();
        select((to + tabs.length) % tabs.length, { focus: true, hash: true });
      });
    });

    /* #patient / #professional in the URL opens that tab directly, so the
       links pointing here can send people to the right form. */
    var wanted = tabs.map(function (t) { return t.dataset.chooserKey; })
                     .indexOf(location.hash.replace('#', ''));
    select(wanted > -1 ? wanted : 0, {});
  });

  /* --- 2. Accordions ------------------------------------------------------ */
  Array.prototype.forEach.call(document.querySelectorAll('.accordion__btn'), function (btn) {
    var panel = document.getElementById(btn.getAttribute('aria-controls'));
    if (!panel) return;

    var setHeight = function (isOpen) {
      panel.style.maxHeight = isOpen ? panel.scrollHeight + 'px' : '0px';
    };

    btn.addEventListener('click', function () {
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      var group = btn.closest('.accordion');

      /* single-open accordions opt in with data-single */
      if (group && group.hasAttribute('data-single') && !isOpen) {
        Array.prototype.forEach.call(group.querySelectorAll('.accordion__btn'), function (other) {
          if (other === btn) return;
          other.setAttribute('aria-expanded', 'false');
          var op = document.getElementById(other.getAttribute('aria-controls'));
          if (op) op.style.maxHeight = '0px';
        });
      }
      btn.setAttribute('aria-expanded', String(!isOpen));
      setHeight(!isOpen);
    });

    if (btn.getAttribute('aria-expanded') === 'true') setHeight(true);
    window.addEventListener('resize', function () {
      if (btn.getAttribute('aria-expanded') === 'true') setHeight(true);
    });
  });

  /* --- 3. Carousel -------------------------------------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-carousel]'), function (root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll('.carousel__slide'));
    var dotsWrap = root.querySelector('.carousel__dots');
    var prev = root.querySelector('[data-carousel-prev]');
    var next = root.querySelector('[data-carousel-next]');
    if (slides.length < 2) return;

    var index = 0, timer = null;
    var interval = parseInt(root.dataset.carouselInterval || '7000', 10);

    var dots = slides.map(function (_, i) {
      if (!dotsWrap) return null;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'carousel__dot';
      b.setAttribute('aria-label', 'Show item ' + (i + 1));
      b.addEventListener('click', function () { go(i); restart(); });
      dotsWrap.appendChild(b);
      return b;
    });

    function go(i) {
      index = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) { s.classList.toggle('is-active', n === index); });
      dots.forEach(function (d, n) { if (d) d.classList.toggle('is-active', n === index); });
    }
    function start() { if (!reduceMotion) timer = setInterval(function () { go(index + 1); }, interval); }
    function stop()  { if (timer) { clearInterval(timer); timer = null; } }
    function restart() { stop(); start(); }

    if (prev) prev.addEventListener('click', function () { go(index - 1); restart(); });
    if (next) next.addEventListener('click', function () { go(index + 1); restart(); });
    root.addEventListener('mouseenter', stop);
    root.addEventListener('mouseleave', start);
    root.addEventListener('focusin', stop);
    root.addEventListener('focusout', start);

    go(0);
    start();
  });

  /* --- 4. Reveal on scroll ------------------------------------------------ */
  var revealables = document.querySelectorAll('[data-reveal]');
  if (revealables.length) {
    if (!('IntersectionObserver' in window) || reduceMotion) {
      Array.prototype.forEach.call(revealables, function (el) { el.classList.add('is-in'); });
    } else {
      var ro = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-in');
          obs.unobserve(entry.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
      Array.prototype.forEach.call(revealables, function (el) { ro.observe(el); });
    }
  }

  /* --- 5. Back to top ----------------------------------------------------- */
  var toTop = document.querySelector('[data-to-top]');
  if (toTop) {
    var toggleTop = function () { toTop.classList.toggle('is-visible', window.scrollY > 700); };
    window.addEventListener('scroll', toggleTop, { passive: true });
    toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: behavior }); });
    toggleTop();
  }

  /* --- 6. Lightbox -------------------------------------------------------- */
  var lb = document.getElementById('lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img');
    Array.prototype.forEach.call(document.querySelectorAll('[data-lightbox]'), function (fig) {
      fig.addEventListener('click', function () {
        var img = fig.querySelector('img');
        if (!img) return;
        lbImg.src = img.currentSrc || img.src;
        lbImg.alt = img.alt || '';
        lb.classList.add('is-open');
        document.body.classList.add('is-locked');
      });
    });
    var closeLb = function () {
      lb.classList.remove('is-open');
      document.body.classList.remove('is-locked');
      lbImg.src = '';
    };
    lb.addEventListener('click', closeLb);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && lb.classList.contains('is-open')) closeLb();
    });
  }

  /* --- 7. Cookie banner --------------------------------------------------- */
  var cookie = document.getElementById('cookieBanner');
  if (cookie) {
    var KEY = 'bdp-cookie-choice';
    var stored = null;
    try { stored = localStorage.getItem(KEY); } catch (err) { stored = null; }

    if (!stored) setTimeout(function () { cookie.classList.add('is-open'); }, 900);

    Array.prototype.forEach.call(cookie.querySelectorAll('[data-cookie-choice]'), function (btn) {
      btn.addEventListener('click', function () {
        try { localStorage.setItem(KEY, btn.dataset.cookieChoice); } catch (err) { /* private mode */ }
        cookie.classList.remove('is-open');
      });
    });
  }
}());
