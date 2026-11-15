// ===== Утилиты =====
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

// ===== 1. Тема =====
const THEME_KEY = 'portfolio_theme';
const themeToggle = $('#theme-toggle');
const themeIcon = themeToggle.querySelector('.theme-icon');

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    themeIcon.textContent = theme === 'dark' ? '🌙' : '☀️';
    themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Включить светлую тему' : 'Включить тёмную тему');
}

function initTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved) {
        applyTheme(saved);
    } else {
        const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
        applyTheme(prefersLight ? 'light' : 'dark');
    }
}

themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
    localStorage.setItem(THEME_KEY, next);
});

initTheme();

// ===== 2. Данные =====
let projects = JSON.parse(localStorage.getItem('portfolio_projects')) || [
    {
        id: 1,
        title: 'Лендинг для кофейни',
        problem: 'Владелец терял клиентов: не было онлайн-меню и записи.',
        solution: 'Сделал одностраничник с меню, картой и формой онлайн-записи.',
        result: 'За первую неделю — 18 записей через сайт.',
        tech: ['HTML', 'CSS', 'JS']
    },
    {
        id: 2,
        title: 'Сайт-визитка фотографа',
        problem: 'Фотограф вёл соцсети, но не имел своего пространства для портфолио.',
        solution: 'Разработал галерею с лайтбоксом и формой заявки.',
        result: 'Клиент отказался от платного конструктора, экономия ~5000₽/год.',
        tech: ['React', 'Tailwind']
    }
];

let messages = JSON.parse(localStorage.getItem('portfolio_messages')) || [];

const saveProjects = () => localStorage.setItem('portfolio_projects', JSON.stringify(projects));
const saveMessages = () => localStorage.setItem('portfolio_messages', JSON.stringify(messages));

// ===== 3. Рендер проектов =====
const projectsGrid = $('#projects-grid');

function renderProjects() {
    projectsGrid.innerHTML = '';
    if (projects.length === 0) {
        projectsGrid.innerHTML = '<p style="text-align:center;grid-column:1/-1;">Пока нет проектов. Добавьте их через админ-панель (⚙️).</p>';
        return;
    }
    projects.forEach(p => {
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'project-card';
        card.setAttribute('aria-label', `Открыть кейс: ${p.title}`);
        card.innerHTML = `
            <button class="delete-btn" data-id="${p.id}" aria-label="Удалить проект ${p.title}" title="Удалить">✕</button>
            <h3>${p.title}</h3>
            <p>${p.problem || p.desc || ''}</p>
            <div class="tech-tags">${(p.tech || []).map(t => `<span class="tech-tag">${t}</span>`).join('')}</div>
        `;
        card.addEventListener('click', (e) => {
            if (e.target.closest('.delete-btn')) return;
            openCase(p);
        });
        projectsGrid.appendChild(card);
    });

    $$('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const id = Number(e.currentTarget.dataset.id);
            if (!confirm('Удалить проект?')) return;
            projects = projects.filter(p => p.id !== id);
            saveProjects();
            renderProjects();
        });
    });
}

// ===== 4. Модалка кейса (с фокус-трапом) =====
const modal = $('#case-modal');
let lastFocused = null;

function openCase(project) {
    lastFocused = document.activeElement;
    $('#case-title').textContent = project.title;
    $('#case-problem').textContent = project.problem || '—';
    $('#case-solution').textContent = project.solution || '—';
    $('#case-result').textContent = project.result || '—';
    $('#case-tech').innerHTML = (project.tech || []).map(t => `<span class="tech-tag">${t}</span>`).join('');
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
    if (e.key === 'Escape') {
        if (!modal.hidden) closeCase();
        else if (!adminPanel.hidden) adminPanel.hidden = true;
    }
    // Фокус-трап в модалке
    if (e.key === 'Tab' && !modal.hidden) {
        const focusable = modal.querySelectorAll('button, [href], input, textarea, [tabindex]:not([tabindex="-1"])');
        if (focusable.length === 0) return;
        const first = focusable[0], last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
});

// ===== 5. Форма =====
const contactForm = $('#contact-form');
const formStatus = $('#form-status');

function validateField(field) {
    let valid = true;
    if (!field.value.trim()) valid = false;
    if (field.type === 'email' && valid) valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value);
    field.setAttribute('aria-invalid', valid ? 'false' : 'true');
    return valid;
}

contactForm.querySelectorAll('input[required], textarea[required]').forEach(f => {
    f.addEventListener('blur', () => validateField(f));
});

contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // honeypot: бот заполнит скрытое поле
    if ($('#website').value) return;

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

    // Сохраняем локально (для админки) — работает всегда
    messages.push({ id: Date.now(), name, email, message, date: new Date().toLocaleString() });
    saveMessages();

    formStatus.textContent = 'Отправляю...';
    formStatus.className = 'form-status';

    /* === РЕАЛЬНАЯ ОТПРАВКА ===
       Зарегистрируйтесь на formspree.io, создайте форму,
       замените YOUR_FORM_ID и раскомментируйте блок ниже.
    try {
        const res = await fetch('https://formspree.io/f/YOUR_FORM_ID', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: JSON.stringify({ name, email, message })
        });
        if (!res.ok) throw new Error('Network error');
        formStatus.textContent = 'Сообщение отправлено! Свяжусь с вами.';
        formStatus.className = 'form-status success';
        contactForm.reset();
    } catch (err) {
        formStatus.textContent = 'Не удалось отправить. Напишите на почту напрямую.';
        formStatus.className = 'form-status error';
        return;
    }
    */

    // демо-режим без бэкенда:
    formStatus.textContent = 'Сообщение отправлено! Свяжусь с вами.';
    formStatus.className = 'form-status success';
    contactForm.reset();
    fields.forEach(f => f.removeAttribute('aria-invalid'));

    if (!adminPanel.hidden) renderMessages();
});

// ===== 6. Админка =====
const adminPanel = $('#admin-panel');

$('#admin-toggle').addEventListener('click', () => {
    adminPanel.hidden = false;
    renderMessages();
    $('#close-admin').focus();
});

$('#close-admin').addEventListener('click', () => { adminPanel.hidden = true; });

$('#add-project-btn').addEventListener('click', () => {
    const title = $('#project-title').value.trim();
    const problem = $('#project-problem').value.trim();
    const solution = $('#project-solution').value.trim();
    const result = $('#project-result').value.trim();
    const techInput = $('#project-tech').value.trim();

    if (!title) { alert('Название обязательно.'); return; }

    projects.push({
        id: Date.now(),
        title,
        problem: problem || '—',
        solution: solution || '—',
        result: result || '—',
        tech: techInput ? techInput.split(',').map(t => t.trim()).filter(Boolean) : ['Без технологий']
    });
    saveProjects();
    renderProjects();
    ['project-title', 'project-problem', 'project-solution', 'project-result', 'project-tech']
        .forEach(id => $('#' + id).value = '');
});

function renderMessages() {
    const list = $('#messages-list');
    list.innerHTML = messages.length === 0
        ? '<p>Сообщений пока нет.</p>'
        : messages.map(m => `
            <div class="message-item">
                <strong>${m.name}</strong> (${m.email})<br>
                <small>${m.date}</small>
                <p>${m.message}</p>
            </div>`).join('');
}

// ===== Старт =====
renderProjects();