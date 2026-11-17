/* =========================================================
   утилиты
========================================================= */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const coarse = matchMedia('(pointer: coarse)').matches;
const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const pad = (n) => String(n).padStart(2, '0');

/* =========================================================
   тема
========================================================= */
const THEME_KEY = 'portfolio_theme';
const themeToggle = $('#theme-toggle');
const metaTheme = $('#meta-theme');

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  metaTheme.setAttribute('content', theme === 'dark' ? '#060A13' : '#F5F7FC');
  themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Включить светлую тему' : 'Включить тёмную тему');
}
applyTheme(localStorage.getItem(THEME_KEY) || 'dark');
themeToggle.addEventListener('click', () => {
  const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  localStorage.setItem(THEME_KEY, next);
});

/* =========================================================
   шапка: прогресс, scrolled, мобильное меню
========================================================= */
const header = $('#site-header');
const progress = $('#progress');
let scrollTick = false;
function onScroll() {
  if (scrollTick) return;
  scrollTick = true;
  requestAnimationFrame(() => {
    const y = window.scrollY;
    header.classList.toggle('scrolled', y > 8);
    const max = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = (max > 0 ? (y / max) * 100 : 0) + '%';
    scrollTick = false;
  });
}
addEventListener('scroll', onScroll, { passive: true });
onScroll();

const menuToggle = $('#menu-toggle');
const mobileMenu = $('#mobile-menu');
function setMenu(open) {
  mobileMenu.classList.toggle('open', open);
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
}
menuToggle.addEventListener('click', () => setMenu(!mobileMenu.classList.contains('open')));
$$('#mobile-menu a').forEach(a => a.addEventListener('click', () => setMenu(false)));
document.addEventListener('click', (e) => {
  if (mobileMenu.classList.contains('open') && !mobileMenu.contains(e.target) && !menuToggle.contains(e.target)) setMenu(false);
});

/* =========================================================
   scrollspy
========================================================= */
const spyLinks = $$('[data-spy]');
const spySections = ['experience', 'projects', 'services', 'skills', 'contact'].map(id => $('#' + id));
if ('IntersectionObserver' in window) {
  const spy = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        spyLinks.forEach(l => l.setAttribute('aria-current', String(l.getAttribute('href') === '#' + en.target.id)));
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px' });
  spySections.forEach(s => s && spy.observe(s));
}

/* =========================================================
   reveal + счётчики
========================================================= */
const revealEls = $$('[data-reveal]');
revealEls.forEach(el => {
  const siblings = [...el.parentElement.children].filter(c => c.hasAttribute('data-reveal'));
  el.style.setProperty('--rd', (siblings.indexOf(el) * 80) + 'ms');
});
function runCounter(el) {
  const target = Number(el.dataset.count);
  const suffix = el.dataset.suffix || '';
  if (reduced) { el.textContent = target + suffix; return; }
  const t0 = performance.now(), dur = 1100;
  (function tick(now) {
    const p = Math.min((now - t0) / dur, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(target * eased) + suffix;
    if (p < 1) requestAnimationFrame(tick);
  })(t0);
}
if ('IntersectionObserver' in window && !reduced) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (!en.isIntersecting) return;
      en.target.classList.add('in');
      $$('[data-count]', en.target).forEach(runCounter);
      if (en.target.hasAttribute('data-count')) runCounter(en.target);
      io.unobserve(en.target);
    });
  }, { threshold: .15 });
  revealEls.forEach(el => io.observe(el));
} else {
  revealEls.forEach(el => el.classList.add('in'));
  $$('[data-count]').forEach(el => { el.textContent = el.dataset.count + (el.dataset.suffix || ''); });
}

/* =========================================================
   терминал: живой прогон проверок
========================================================= */
const termBody = $('#term-body');
const SCRIPT = [
  { t: '$ qa run --target portfolio', c: 't-cmd', type: true },
  { t: '✓ вёрстка и адаптив ......... PASS', c: 't-green' },
  { t: '✓ доступность (a11y) ........ PASS', c: 't-green' },
  { t: '✓ api-контракты ............. PASS', c: 't-green' },
  { t: '✓ форма и интеграции ........ PASS', c: 't-green' },
  { t: '$ git push origin main', c: 't-cmd', type: true },
  { t: '→ github pages: deploy ok', c: 't-cyan' },
  { t: 'status: OPEN TO WORK ●', c: 't-amber' }
];
function termLine(text, cls) {
  const span = document.createElement('span');
  span.className = 'term-line ' + (cls || '');
  span.textContent = text;
  termBody.appendChild(span);
  return span;
}
async function terminalLoop() {
  if (reduced) { SCRIPT.forEach(l => termLine(l.t, l.c)); return; }
  const caret = document.createElement('span');
  caret.className = 'caret';
  while (true) {
    termBody.innerHTML = '';
    for (const line of SCRIPT) {
      if (line.type) {
        const span = termLine('', line.c);
        span.appendChild(caret);
        for (const ch of line.t) {
          caret.before(document.createTextNode(ch));
          await sleep(26);
        }
        await sleep(240);
      } else {
        termLine(line.t, line.c);
        await sleep(230);
      }
    }
    termBody.appendChild(caret);
    await sleep(3200);
    while (document.hidden) await sleep(600);
  }
}
terminalLoop();

/* =========================================================
   tilt ID-карточки
========================================================= */
const idCard = $('#id-card');
if (idCard && !coarse && !reduced) {
  let raf = null;
  idCard.addEventListener('pointermove', (e) => {
    if (raf) return;
    raf = requestAnimationFrame(() => {
      const r = idCard.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - .5;
      const y = (e.clientY - r.top) / r.height - .5;
      idCard.style.transform = `perspective(900px) rotateY(${x * 7}deg) rotateX(${-y * 7}deg)`;
      raf = null;
    });
  });
  idCard.addEventListener('pointerleave', () => { idCard.style.transform = ''; });
}

/* =========================================================
   проекты: загрузка, фильтры, рендер
========================================================= */
const CATS = { qa: 'QA', backend: 'BACKEND', web: 'WEB', support: 'SUPPORT' };
const FILTERS = [
  { id: 'all', label: 'все' },
  { id: 'qa', label: 'qa' },
  { id: 'backend', label: 'backend' },
  { id: 'web', label: 'web' },
  { id: 'support', label: 'support' }
];
const state = { projects: [], view: [], filter: 'all', modalIndex: 0 };
const grid = $('#projects-grid');
const filtersBox = $('#filters');
const filterCount = $('#filter-count');

async function loadProjects() {
  grid.innerHTML = '<p class="grid-note">загрузка кейсов…</p>';
  try {
    const res = await fetch('projects.json');
    if (!res.ok) throw new Error('HTTP ' + res.status);
    state.projects = await res.json();
    renderFilters();
    applyFilter(state.filter);
  } catch (err) {
    console.error('Ошибка загрузки projects.json:', err);
    grid.innerHTML = '<div class="grid-note">не удалось загрузить кейсы<br><button class="btn btn-secondary btn-sm mono" id="retry-load" type="button">повторить</button></div>';
    $('#retry-load').addEventListener('click', loadProjects);
  }
}
function renderFilters() {
  filtersBox.innerHTML = '';
  FILTERS.forEach(f => {
    const count = f.id === 'all' ? state.projects.length : state.projects.filter(p => p.category === f.id).length;
    if (f.id !== 'all' && count === 0) return;
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'filter-chip';
    btn.setAttribute('aria-pressed', String(state.filter === f.id));
    btn.innerHTML = `${f.label}<span class="cnt">${count}</span>`;
    btn.addEventListener('click', () => applyFilter(f.id));
    filtersBox.appendChild(btn);
  });
}
function applyFilter(id) {
  state.filter = id;
  state.view = id === 'all' ? [...state.projects] : state.projects.filter(p => p.category === id);
  $$('.filter-chip', filtersBox).forEach((b, i) => {
    const f = FILTERS.filter(x => x.id === 'all' || state.projects.some(p => p.category === x.id))[i];
    if (f) b.setAttribute('aria-pressed', String(f.id === id));
  });
  filterCount.textContent = `// показано ${state.view.length} из ${state.projects.length}`;
  renderGrid();
}
function renderGrid() {
  grid.innerHTML = '';
  if (!state.view.length) {
    grid.innerHTML = '<p class="grid-note">в этой категории пока пусто</p>';
    return;
  }
  state.view.forEach((p, i) => {
    const card = document.createElement('article');
    card.className = 'case-card';
    card.style.setProperty('--d', (i * 70) + 'ms');
    card.innerHTML = `
      <div class="case-media">
        <span class="case-index">CASE-${pad(p.id)}</span>
        <span class="chip-cat">${CATS[p.category] || 'CASE'}</span>
        <img src="${p.image}" alt="Иллюстрация кейса: ${p.title}" loading="lazy" width="400" height="225">
      </div>
      <div class="case-body">
        <h3 class="disp">${p.title}</h3>
        <p class="case-problem">${p.problem}</p>
        <span class="case-metric"><svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>${p.metric || p.result}</span>
        <div class="chips">${(p.tech || []).slice(0, 4).map(t => `<span>${t}</span>`).join('')}</div>
        <button class="case-open" type="button" aria-label="Открыть кейс: ${p.title}">открыть кейс
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </button>
      </div>`;
    $('.case-open', card).addEventListener('click', () => openCase(i));
    grid.appendChild(card);
  });
}

/* =========================================================
   модалка кейса
========================================================= */
const modal = $('#case-modal');
const modalContent = $('.modal-content', modal);
let lastFocused = null;

function fillCase(i) {
  const p = state.view[i];
  if (!p) return;
  state.modalIndex = i;
  $('#case-index').textContent = 'CASE-' + pad(p.id);
  $('#case-cat').textContent = CATS[p.category] || 'CASE';
  $('#case-title').textContent = p.title;
  $('#case-problem').textContent = p.problem || '—';
  $('#case-solution').textContent = p.solution || '—';
  $('#case-result').textContent = p.result || '—';
  $('#case-tech').innerHTML = (p.tech || []).map(t => `<span>${t}</span>`).join('');
  $('#case-counter').textContent = `${i + 1} / ${state.view.length}`;
  const img = $('#case-image');
  if (p.image) { img.src = p.image; img.alt = 'Иллюстрация кейса: ' + p.title; img.hidden = false; }
  else { img.hidden = true; img.removeAttribute('src'); }
  const single = state.view.length < 2;
  $('#case-prev').disabled = single;
  $('#case-next').disabled = single;
  modalContent.scrollTop = 0;
}
function openCase(i) {
  lastFocused = document.activeElement;
  fillCase(i);
  modal.hidden = false;
  document.documentElement.classList.add('locked');
  $('.modal-close', modal).focus();
}
function closeCase() {
  modal.hidden = true;
  document.documentElement.classList.remove('locked');
  if (lastFocused) lastFocused.focus();
}
function stepCase(dir) {
  const n = state.view.length;
  if (n < 2) return;
  fillCase((state.modalIndex + dir + n) % n);
}
$('#case-prev').addEventListener('click', () => stepCase(-1));
$('#case-next').addEventListener('click', () => stepCase(1));
modal.addEventListener('click', (e) => { if (e.target.hasAttribute('data-close')) closeCase(); });
document.addEventListener('keydown', (e) => {
  if (!modal.hidden) {
    if (e.key === 'Escape') closeCase();
    else if (e.key === 'ArrowRight') stepCase(1);
    else if (e.key === 'ArrowLeft') stepCase(-1);
    else if (e.key === 'Tab') {
      const f = $$('button:not([disabled]), [href]', modalContent);
      if (!f.length) return;
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  } else if (e.key === 'Escape' && mobileMenu.classList.contains('open')) {
    setMenu(false);
  }
});

/* =========================================================
   форма (FormSubmit.co)
========================================================= */
const contactForm = $('#contact-form');
const formStatus = $('#form-status');
const submitBtn = $('#submit-btn');

function validateField(field) {
  let valid = field.value.trim().length > 0;
  if (valid && field.type === 'email') valid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(field.value);
  field.setAttribute('aria-invalid', String(!valid));
  return valid;
}
$$('input[required], textarea[required]', contactForm).forEach(f => {
  f.addEventListener('blur', () => validateField(f));
  f.addEventListener('input', () => { if (f.getAttribute('aria-invalid') === 'true') validateField(f); });
});
contactForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  if ($('#website').value) return;
  const fields = [$('#name'), $('#email'), $('#message')];
  const results = fields.map(validateField);
  if (results.includes(false)) {
    formStatus.textContent = '// проверьте выделенные поля';
    formStatus.className = 'form-status mono error';
    fields[results.indexOf(false)].focus();
    return;
  }
  submitBtn.disabled = true;
  submitBtn.classList.add('loading');
  $('.btn-label', submitBtn).textContent = 'Отправка…';
  formStatus.textContent = '';
  try {
    const res = await fetch(contactForm.action, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({
        name: $('#name').value.trim(),
        email: $('#email').value.trim(),
        message: $('#message').value.trim(),
        _subject: 'Новая заявка с портфолио!',
        _captcha: 'true',
        _template: 'table'
      })
    });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    formStatus.textContent = '✓ отправлено — отвечу в течение дня';
    formStatus.className = 'form-status mono success';
    contactForm.reset();
    fields.forEach(f => f.removeAttribute('aria-invalid'));
    toast('сообщение ушло на почту ✓');
  } catch (err) {
    console.error('Ошибка отправки:', err);
    formStatus.textContent = '// не вышло — напишите на blvxx@ya.ru';
    formStatus.className = 'form-status mono error';
  } finally {
    submitBtn.disabled = false;
    submitBtn.classList.remove('loading');
    $('.btn-label', submitBtn).textContent = 'Отправить сообщение';
  }
});

/* =========================================================
   toast + копирование email
========================================================= */
const toastEl = $('#toast');
let toastTimer;
function toast(msg) {
  toastEl.textContent = msg;
  toastEl.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toastEl.classList.remove('show'), 2400);
}
$$('[data-copy]').forEach(btn => btn.addEventListener('click', async () => {
  const text = btn.dataset.copy;
  try {
    await navigator.clipboard.writeText(text);
    toast('email скопирован ✓');
  } catch {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); toast('email скопирован ✓'); }
    catch { toast('не удалось скопировать'); }
    ta.remove();
  }
}));

/* =========================================================
   футер
========================================================= */
$('#year').textContent = new Date().getFullYear();
$('#to-top').addEventListener('click', () => scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }));

/* =========================================================
   старт
========================================================= */
loadProjects();
