/* =========================================================
Утилиты
========================================================= */
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

/* =========================================================
ТЕМА (светлая / тёмная)
========================================================= */
const THEME_KEY = 'portfolio_theme';
const themeToggle = $('#theme-toggle');
const themeIcon = themeToggle.querySelector('.theme-icon');

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  themeIcon.textContent = theme === 'dark' ? '🌙' : '☀️';
  themeToggle.setAttribute('aria-label',
    theme === 'dark' ? 'Включить светлую тему' : 'Включить тёмную тему');
}

function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved) {
    applyTheme(saved);
  } else {
    applyTheme('light');
  }
}

themeToggle.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  localStorage.setItem(THEME_KEY, next);
});

initTheme();

/* =========================================================
ДАННЫЕ (проекты из JSON)
========================================================= */
let projects = [];

async function loadProjects() {
  try {
    const response = await fetch('projects.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    projects = await response.json();
  } catch (error) {
    console.error('Ошибка загрузки projects.json:', error);
    projects = [];
  }
  renderProjects();
}

/* =========================================================
РЕНДЕР ПРОЕКТОВ
========================================================= */
const projectsGrid = $('#projects-grid');

function renderProjects() {
  projectsGrid.innerHTML = '';

  if (projects.length === 0) {
    projectsGrid.innerHTML =
      '<p style="text-align:center;grid-column:1/-1;">Проекты не найдены. Проверьте projects.json.</p>';
    return;
  }

  projects.forEach(p => {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'project-card';
    card.setAttribute('aria-label', `Открыть кейс: ${p.title}`);

    const imgHTML = p.image
      ? `<img class="project-image" src="${p.image}" alt="Скриншот проекта ${p.title}" loading="lazy" width="400" height="225">`
      : '';

    card.innerHTML = `
      ${imgHTML}
      <div class="project-card-body">
        <h3>${p.title}</h3>
        <p>${p.problem || ''}</p>
        <div class="tech-tags">${(p.tech || []).map(t => `<span class="tech-tag">${t}</span>`).join('')}</div>
      </div>
    `;

    card.addEventListener('click', () => {
      openCase(p);
    });

    projectsGrid.appendChild(card);
  });
}

/* =========================================================
МОДАЛКА КЕЙСА
========================================================= */
const modal = $('#case-modal');
let lastFocused = null;

function openCase(project) {
  lastFocused = document.activeElement;

  $('#case-title').textContent = project.title;
  $('#case-problem').textContent = project.problem || '—';
  $('#case-solution').textContent = project.solution || '—';
  $('#case-result').textContent = project.result || '—';
  $('#case-tech').innerHTML = (project.tech || [])
    .map(t => `<span class="tech-tag">${t}</span>`).join('');

  const img = $('#case-image');
  if (project.image) {
    img.src = project.image;
    img.alt = `Скриншот проекта ${project.title}`;
    img.hidden = false;
  } else {
    img.hidden = true;
    img.removeAttribute('src');
  }

  modal.hidden = false;
  document.body.style.overflow = 'hidden';
  modal.querySelector('.modal-close').focus();
}

function closeCase() {
  modal.hidden = true;
  document.body.style.overflow = '';
  if (lastFocused) lastFocused.focus();
}

modal.addEventListener('click', (e) => {
  if (e.target.hasAttribute('data-close')) closeCase();
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && !modal.hidden) {
    closeCase();
  }

  if (e.key === 'Tab' && !modal.hidden) {
    const focusable = modal.querySelectorAll(
      'button, [href], input, textarea, [tabindex]:not([tabindex="-1"])'
    );
    if (focusable.length === 0) return;
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }
});

/* =========================================================
ФОРМА ОБРАТНОЙ СВЯЗИ (FormSubmit.co)
========================================================= */
const contactForm = $('#contact-form');
const formStatus = $('#form-status');

function validateField(field) {
  let valid = true;
  if (!field.value.trim()) valid = false;
  if (field.type === 'email' && valid) {
    valid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(field.value);
  }
  field.setAttribute('aria-invalid', valid ? 'false' : 'true');
  return valid;
}

contactForm.querySelectorAll('input[required], textarea[required]').forEach(f => {
  f.addEventListener('blur', () => validateField(f));
});

contactForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  if ($('#website').value) return; // honeypot

  const name = $('#name').value.trim();
  const email = $('#email').value.trim();
  const message = $('#message').value.trim();
  const fields = [$('#name'), $('#email'), $('#message')];

  const allValid = fields.map(validateField).every(Boolean);
  if (!allValid) {
    formStatus.textContent = 'Проверьте поля формы.';
    formStatus.className = 'form-status error';
    return;
  }

  const submitBtn = contactForm.querySelector('button[type="submit"]');
  const originalText = submitBtn.textContent;
  submitBtn.disabled = true;
  submitBtn.textContent = 'Отправка...';

  try {
    const response = await fetch(contactForm.action, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        name,
        email,
        message,
        _subject: 'Новая заявка с портфолио!',
        _captcha: 'true',
        _template: 'table'
      })
    });

    if (!response.ok) throw new Error('Ошибка сервера');

    formStatus.textContent = 'Сообщение отправлено! Свяжусь с вами в течение дня.';
    formStatus.className = 'form-status success';
    contactForm.reset();
    fields.forEach(f => f.removeAttribute('aria-invalid'));

  } catch (error) {
    console.error('Ошибка отправки:', error);
    formStatus.textContent = 'Не удалось отправить. Напишите напрямую на blvxx@ya.ru';
    formStatus.className = 'form-status error';
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = originalText;
  }
});

/* =========================================================
ПЛАВНОЕ ПОЯВЛЕНИЕ СЕКЦИЙ ПРИ СКРОЛЛЕ
========================================================= */
(function initReveal() {
  const targets = document.querySelectorAll('.section, .hero-inner, .site-footer');
  if (!('IntersectionObserver' in window) || targets.length === 0) return;

  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  targets.forEach(el => {
    el.classList.add('reveal');
    io.observe(el);
  });
})();

/* =========================================================
СТАРТ
========================================================= */
loadProjects();
