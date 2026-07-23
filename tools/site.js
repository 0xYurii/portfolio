/* Younes Hebaiche — portfolio. Theme, i18n (en/fr/ar + RTL), menu, copy, year. */
(function () {
  'use strict';
  var doc = document.documentElement;
  var I18N = window.__I18N__ || { en:{}, fr:{}, ar:{} };

  /* ---------- theme ---------- */
  var toggle = document.getElementById('theme-toggle');
  function theme(){ return doc.getAttribute('data-scheme') === 'light' ? 'light' : 'dark'; }
  if (toggle) toggle.addEventListener('click', function () {
    var next = theme() === 'light' ? 'dark' : 'light';
    doc.setAttribute('data-scheme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });

  /* ---------- i18n ---------- */
  function detectLang(){
    try { var s = localStorage.getItem('lang'); if (s === 'en' || s === 'fr' || s === 'ar') return s; } catch (e) {}
    var n = (navigator.language || 'en').slice(0,2).toLowerCase();
    return (n === 'fr' || n === 'ar') ? n : 'en';
  }
  var curLang = 'en';
  function applyLang(l){
    if (!I18N[l]) l = 'en';
    curLang = l;
    var dict = I18N[l] || {};
    doc.setAttribute('lang', l);
    doc.setAttribute('dir', l === 'ar' ? 'rtl' : 'ltr');
    var nodes = document.querySelectorAll('[data-i18n]');
    for (var i = 0; i < nodes.length; i++){
      var k = nodes[i].getAttribute('data-i18n');
      if (dict[k] != null) nodes[i].textContent = dict[k];
    }
    var arias = document.querySelectorAll('[data-i18n-aria]');
    for (var j = 0; j < arias.length; j++){
      var ak = arias[j].getAttribute('data-i18n-aria');
      if (dict[ak] != null) arias[j].setAttribute('aria-label', dict[ak]);
    }
    var btns = document.querySelectorAll('.lang-btn');
    for (var b = 0; b < btns.length; b++)
      btns[b].classList.toggle('active', btns[b].getAttribute('data-lang') === l);
  }
  var langBtns = document.querySelectorAll('.lang-btn');
  for (var i = 0; i < langBtns.length; i++){
    langBtns[i].addEventListener('click', function () {
      var l = this.getAttribute('data-lang');
      try { localStorage.setItem('lang', l); } catch (e) {}
      applyLang(l);
    });
  }
  applyLang(detectLang());

  /* ---------- mobile menu ---------- */
  var menuBtn = document.getElementById('menu-btn');
  var nav = document.getElementById('nav');
  if (menuBtn && nav){
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e){
      if (e.target.closest('a')){ nav.classList.remove('open'); menuBtn.setAttribute('aria-expanded','false'); }
    });
  }

  /* ---------- copy email ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('.copy-btn'), function (btn){
    var label = btn.querySelector('.copy-label');
    var timer;
    function msg(key){ return (I18N[curLang] && I18N[curLang][key]) || (I18N.en && I18N.en[key]) || key; }
    function flash(key){
      if (label){ label.textContent = msg(key); label.removeAttribute('data-i18n'); }
      btn.classList.add('copied');
      clearTimeout(timer);
      timer = setTimeout(function (){
        btn.classList.remove('copied');
        if (label){ label.textContent = msg('contact.copy'); label.setAttribute('data-i18n','contact.copy'); }
      }, 1700);
    }
    btn.addEventListener('click', function (){
      var v = btn.getAttribute('data-copy');
      if (navigator.clipboard && navigator.clipboard.writeText)
        navigator.clipboard.writeText(v).then(function (){ flash('contact.copied'); }, fallback);
      else fallback();
      function fallback(){
        try {
          var ta = document.createElement('textarea'); ta.value = v; ta.style.position='fixed'; ta.style.left='-9999px';
          document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
          flash('contact.copied');
        } catch (e){ flash('contact.copyfail'); }
      }
    });
  });

  /* ---------- year ---------- */
  var y = document.getElementById('year'); if (y) y.textContent = String(new Date().getFullYear());
})();
