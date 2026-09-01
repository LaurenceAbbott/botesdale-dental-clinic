/* =============================================================================
   forms.js — progressive client-side validation, multi-step forms, repeat groups
   -----------------------------------------------------------------------------
   Three behaviours, all opt-in via data attributes and all progressive — with
   JavaScript off, a form is a single long page that still submits.

     [data-validate]  Validated on submit and, once a field has been touched,
                      on blur. See validateField().
     [data-steps]     The form's [data-step] panels become a wizard: one panel
                      at a time, a stepper across the top, Back / Continue
                      below. Without JS every panel is simply visible.
     [data-repeat]    A repeatable group ("add another entitled person"). The
                      first item is in the markup; further ones are cloned from
                      the <template>. Fields are named  base[i][suffix]  so a
                      back end receives a clean array.

   >>> TO GO LIVE <<<
   Pick one of these and the rest of the file stays as it is:
     1. Formspree  — set action="https://formspree.io/f/XXXX" method="post"
                     on the <form> and delete the `e.preventDefault()` branch
                     inside the submit handler (keep the validation call).
     2. Netlify    — add  netlify  and  name="..."  to the <form> element.
     3. Own endpoint — replace the SUCCESS block below with a fetch() POST.

   Note for multi-step forms: every step stays in the DOM, so a normal form
   POST sends all of the fields regardless of which step is on screen.
   ========================================================================== */
(function () {
  'use strict';

  var EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var PHONE = /^[0-9\s()+.-]{7,}$/;

  function toArray(list) { return Array.prototype.slice.call(list); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function escapeRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  function reducedMotion() {
    return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  /* Every user-editable control inside a scope. */
  function controlsIn(scope) {
    return toArray(scope.querySelectorAll('input, select, textarea')).filter(function (el) {
      return el.type !== 'hidden' && el.type !== 'submit' && el.type !== 'button' && !el.disabled;
    });
  }

  /* ---------------------------------------------------------------------------
     Validation
     ------------------------------------------------------------------------ */
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

  /* Validates a scope (a step, or the whole form) and returns the first
     control that failed, or null. */
  function validateScope(scope) {
    var firstBad = null;
    controlsIn(scope).forEach(function (input) {
      input.dataset.touched = '1';
      if (!validateField(input) && !firstBad) firstBad = input;
    });
    return firstBad;
  }

  /* Wires blur/input validation onto controls that have not been wired yet.
     Safe to call again after cloning new fields in. */
  function wireControls(scope) {
    controlsIn(scope).forEach(function (input) {
      if (input.dataset.wired) return;
      input.dataset.wired = '1';

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
  }

  /* ---------------------------------------------------------------------------
     Repeat groups — [data-repeat]
     ------------------------------------------------------------------------ */
  function repeatItems(root) {
    return toArray(root.querySelectorAll('[data-repeat-item]'));
  }

  /* Rewrites id / name / for / aria-* so the items are always numbered 0..n-1
     with no gaps, and refreshes each item's visible number. */
  function renumber(root) {
    var base = root.getAttribute('data-repeat-name') || 'item';
    var byId = new RegExp('^(' + escapeRe(base) + ')-\\d+-');
    var byName = new RegExp('^(' + escapeRe(base) + ')\\[\\d+\\]');

    repeatItems(root).forEach(function (item, i) {
      toArray(item.querySelectorAll('[id], [name], [for], [aria-controls], [aria-describedby]'))
        .forEach(function (el) {
          ['id', 'name', 'for', 'aria-controls', 'aria-describedby'].forEach(function (attr) {
            var v = el.getAttribute(attr);
            if (!v) return;
            el.setAttribute(attr, v.replace(byId, '$1-' + i + '-').replace(byName, '$1[' + i + ']'));
          });
        });

      var num = item.querySelector('[data-repeat-num]');
      if (num) num.textContent = pad(i + 1);
    });

    refreshRepeatState(root);
  }

  function refreshRepeatState(root) {
    var items = repeatItems(root);
    var min = parseInt(root.getAttribute('data-repeat-min') || '1', 10);
    var max = parseInt(root.getAttribute('data-repeat-max') || '0', 10);
    var add = root.querySelector('[data-repeat-add]');

    /* The remove control disappears rather than greys out when an item is the
       last one standing — there is nothing useful it could do. */
    items.forEach(function (item) {
      var btn = item.querySelector('[data-repeat-remove]');
      if (btn) btn.hidden = items.length <= min;
    });

    if (add) {
      var full = max > 0 && items.length >= max;
      add.hidden = full;
      var note = root.querySelector('[data-repeat-full]');
      if (note) note.hidden = !full;
    }
  }

  function announce(root, text) {
    var live = root.querySelector('[data-repeat-status]');
    if (live) live.textContent = text;
  }

  function initRepeat(root) {
    var tpl = root.querySelector('[data-repeat-template]');
    var list = root.querySelector('[data-repeat-list]');
    var add = root.querySelector('[data-repeat-add]');
    var singular = root.getAttribute('data-repeat-singular') || 'item';
    if (!tpl || !list) return;

    if (add) {
      add.addEventListener('click', function () {
        var max = parseInt(root.getAttribute('data-repeat-max') || '0', 10);
        if (max > 0 && repeatItems(root).length >= max) return;

        var index = repeatItems(root).length;
        var html = tpl.innerHTML.replace(/__i__/g, String(index))
                                .replace(/__n__/g, pad(index + 1));
        var frame = document.createElement('div');
        frame.innerHTML = html;
        var item = frame.querySelector('[data-repeat-item]');
        if (!item) return;

        list.appendChild(item);
        renumber(root);
        wireControls(item);

        var first = controlsIn(item)[0];
        if (first) {
          first.focus();
          if (!reducedMotion()) item.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        announce(root, singular + ' ' + repeatItems(root).length + ' added.');
      });
    }

    list.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-repeat-remove]');
      if (!btn || !list.contains(btn)) return;

      var items = repeatItems(root);
      var min = parseInt(root.getAttribute('data-repeat-min') || '1', 10);
      if (items.length <= min) return;

      var item = btn.closest('[data-repeat-item]');
      var at = items.indexOf(item);
      item.parentNode.removeChild(item);
      renumber(root);

      /* Focus the next item's remove button, or the add button, so keyboard
         users are not dropped back at the top of the document. */
      var left = repeatItems(root);
      var next = left[Math.min(at, left.length - 1)];
      var target = (next && !next.querySelector('[data-repeat-remove]').hidden)
        ? next.querySelector('[data-repeat-remove]')
        : (add && !add.hidden ? add : null);
      if (target) target.focus();

      announce(root, singular + ' removed. ' + left.length + ' remaining.');
    });

    renumber(root);
  }

  /* ---------------------------------------------------------------------------
     Multi-step — [data-steps]
     ------------------------------------------------------------------------ */
  function initSteps(form) {
    var steps = toArray(form.querySelectorAll('[data-step]'));
    var actions = form.querySelector('.form__actions');
    if (steps.length < 2 || !actions) return null;

    var furthest = 0;
    var current = 0;
    var id = form.id || 'form';

    /* --- stepper ------------------------------------------------------- */
    var nav = document.createElement('nav');
    nav.className = 'stepper';
    nav.setAttribute('aria-label', 'Form progress');
    nav.innerHTML =
      '<p class="stepper__count" data-step-count></p>' +
      '<ol class="stepper__list">' +
      steps.map(function (step, i) {
        return '<li class="stepper__item"><button class="stepper__btn" type="button" ' +
               'data-step-to="' + i + '"><span class="stepper__num" aria-hidden="true">' +
               pad(i + 1) + '</span><span class="stepper__label">' +
               (step.getAttribute('data-step-title') || 'Step ' + (i + 1)) +
               '</span></button></li>';
      }).join('') +
      '</ol>' +
      '<div class="stepper__bar"><span data-step-bar></span></div>';
    form.insertBefore(nav, form.firstChild);

    var countEl = nav.querySelector('[data-step-count]');
    var barEl = nav.querySelector('[data-step-bar]');
    var stepBtns = toArray(nav.querySelectorAll('[data-step-to]'));

    /* --- step navigation -------------------------------------------------
       Back, Continue and Submit share the one action row: only one of
       Continue / Submit is ever shown, so the form never grows a second
       button row (and a second rule above it) on the last step. */
    var submitBtn = actions.querySelector('[type="submit"]');
    var note = actions.querySelector('.form__note');

    /* Continue is the primary action of the step, so it matches whatever the
       form's submit is. On a page carrying two forms only one of them is the
       page's primary; the other is marked outline and its Continue follows,
       so the page never shows two primaries at once. */
    var stepVariant = form.dataset.stepVariant || 'solid';

    var navFrame = document.createElement('div');
    navFrame.innerHTML =
      '<button class="btn btn--outline btn--sm" type="button" data-step-back>' +
      '<span class="btn__label">Back</span></button>' +
      '<button class="btn btn--' + stepVariant + '" type="button" data-step-next>' +
      '<span class="btn__label">Continue</span></button>';

    var backBtn = navFrame.firstChild;
    var nextBtn = navFrame.lastChild;
    actions.insertBefore(backBtn, submitBtn);
    actions.insertBefore(nextBtn, submitBtn);

    var live = document.createElement('p');
    live.className = 'visually-hidden';
    live.setAttribute('role', 'status');
    form.appendChild(live);

    steps.forEach(function (step, i) {
      step.id = step.id || id + '-step-' + i;
      step.setAttribute('role', 'group');
      step.setAttribute('aria-label', step.getAttribute('data-step-title') || 'Step ' + (i + 1));
      step.setAttribute('tabindex', '-1');
    });

    form.classList.add('form--stepped');

    function show(i, opts) {
      var last = steps.length - 1;
      current = Math.max(0, Math.min(i, last));
      furthest = Math.max(furthest, current);

      steps.forEach(function (step, n) { step.hidden = n !== current; });

      stepBtns.forEach(function (btn, n) {
        var item = btn.parentNode;
        item.classList.toggle('is-current', n === current);
        item.classList.toggle('is-done', n < furthest && n !== current);
        /* Only steps already reached are reachable — jumping ahead would skip
           validation of everything in between. */
        btn.disabled = n > furthest;
        if (n === current) { btn.setAttribute('aria-current', 'step'); }
        else { btn.removeAttribute('aria-current'); }
      });

      var title = steps[current].getAttribute('data-step-title') || '';
      countEl.textContent = 'Step ' + (current + 1) + ' of ' + steps.length;
      barEl.style.width = ((current + 1) / steps.length * 100) + '%';

      backBtn.hidden = current === 0;
      nextBtn.hidden = current === last;
      if (submitBtn) submitBtn.hidden = current !== last;
      if (note) note.hidden = current !== last;

      /* Restart the entrance animation — unhiding an element that is already
         in the DOM will not replay it on its own. */
      var panel = steps[current];
      panel.classList.remove('is-entering');
      void panel.offsetWidth;
      panel.classList.add('is-entering');

      if (opts && opts.focus !== false) {
        steps[current].focus();
        live.textContent = 'Step ' + (current + 1) + ' of ' + steps.length + ', ' +
                           (steps[current].getAttribute('data-step-title') || '') + '.';
        var top = nav.getBoundingClientRect().top + window.pageYOffset - 100;
        window.scrollTo({ top: Math.max(0, top), behavior: reducedMotion() ? 'auto' : 'smooth' });
      }
    }

    function advance() {
      var bad = validateScope(steps[current]);
      if (bad) {
        bad.focus();
        if (!reducedMotion()) bad.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }
      show(current + 1);
    }

    nextBtn.addEventListener('click', advance);
    backBtn.addEventListener('click', function () { show(current - 1); });

    stepBtns.forEach(function (btn, n) {
      btn.addEventListener('click', function () {
        if (n > furthest) return;
        /* Moving forward through the stepper still validates what is on screen;
           moving back never blocks. */
        if (n > current && validateScope(steps[current])) { advance(); return; }
        show(n);
      });
    });

    /* Enter in a text field should advance rather than submit, except on the
       last step where submitting is what the user means. Buttons are left
       alone — Enter on "Add another person" must add a person. */
    form.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter' || current === steps.length - 1) return;
      var tag = e.target.tagName;
      if (tag === 'TEXTAREA' || tag === 'BUTTON' || tag === 'A') return;
      e.preventDefault();
      advance();
    });

    show(0, { focus: false });

    return {
      /* Called on submit failure: surface the step holding the first error. */
      revealFor: function (input) {
        for (var i = 0; i < steps.length; i++) {
          if (steps[i].contains(input)) {
            furthest = Math.max(furthest, i);
            show(i, { focus: false });
            return;
          }
        }
      }
    };
  }

  /* ---------------------------------------------------------------------------
     Boot
     ------------------------------------------------------------------------ */
  toArray(document.querySelectorAll('[data-repeat]')).forEach(initRepeat);

  toArray(document.querySelectorAll('[data-validate]')).forEach(function (form) {
    wireControls(form);

    var wizard = form.hasAttribute('data-steps') ? initSteps(form) : null;

    form.addEventListener('submit', function (e) {
      var firstBad = validateScope(form);

      if (firstBad) {
        e.preventDefault();
        if (wizard) wizard.revealFor(firstBad);
        firstBad.focus();
        if (!reducedMotion()) firstBad.scrollIntoView({ behavior: 'smooth', block: 'center' });
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
        success.scrollIntoView({ behavior: reducedMotion() ? 'auto' : 'smooth', block: 'center' });
      }
    });
  });
}());
