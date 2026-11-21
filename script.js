const $ = (selector, root = document) => root.querySelector(selector);
const grid = $('#projects-grid');
const filtersEl = $('#project-filters');
const countEl = $('#project-count');
const filters = [
  {id:'all',label:'Все проекты'},
  {id:'web',label:'Веб-разработка'},
  {id:'qa',label:'QA / API'},
  {id:'support',label:'Поддержка / инциденты'},
  {id:'analytics',label:'Аналитика'},
  {id:'prototype',label:'Прототипы'}
];
let activeFilter = 'all';
let projects = [];

function renderFilters(){
  filtersEl.innerHTML = '';
  filters.forEach(filter => {
    const count = filter.id === 'all' ? projects.length : projects.filter(project => project.category === filter.id).length;
    if (!count) return;
    const button = document.createElement('button');
    button.className = 'filter-btn';
    button.type = 'button';
    button.textContent = filter.label;
    button.setAttribute('aria-pressed', String(activeFilter === filter.id));
    button.addEventListener('click', () => {
      activeFilter = filter.id;
      renderFilters();
      renderProjects();
    });
    filtersEl.appendChild(button);
  });
}
function renderProjects(){
  const visible = activeFilter === 'all' ? projects : projects.filter(project => project.category === activeFilter);
  countEl.textContent = String(visible.length).padStart(2,'0') + ' / ' + String(projects.length).padStart(2,'0');
  grid.innerHTML = '';
  if (!visible.length){
    const empty = document.createElement('p');
    empty.className = 'loading';
    empty.textContent = 'В этой категории пока нет проектов.';
    grid.appendChild(empty);
    return;
  }
  visible.forEach(project => {
    const card = document.createElement('article');
    card.className = 'project-card';
    const top = document.createElement('div');
    top.className = 'project-top';
    const kicker = document.createElement('span');
    kicker.className = 'project-kicker';
    kicker.textContent = project.kicker;
    const number = document.createElement('span');
    number.className = 'project-number';
    number.textContent = String(project.id).padStart(2,'0');
    const title = document.createElement('h3');
    title.textContent = project.title;
    top.append(kicker, number, title);
    const body = document.createElement('div');
    body.className = 'project-body';
    const description = document.createElement('p');
    description.className = 'project-description';
    description.textContent = project.description;
    body.appendChild(description);
    const list = document.createElement('ul');
    list.className = 'project-highlights';
    project.highlights.forEach(item => {
      const li = document.createElement('li');
      li.textContent = item;
      list.appendChild(li);
    });
    body.appendChild(list);
    const tags = document.createElement('div');
    tags.className = 'project-tags';
    project.tech.forEach(item => {
      const tag = document.createElement('span');
      tag.className = 'project-tag';
      tag.textContent = item;
      tags.appendChild(tag);
    });
    body.appendChild(tags);
    const footer = document.createElement('div');
    footer.className = 'project-footer';
    const status = document.createElement('span');
    status.className = 'project-status';
    status.textContent = project.status;
    const link = document.createElement('a');
    link.className = 'project-link';
    link.href = project.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = project.link + ' ↗';
    footer.append(status, link);
    body.appendChild(footer);
    card.append(top, body);
    grid.appendChild(card);
  });
}
async function init(){
  try{
    const response = await fetch('projects.json');
    if (!response.ok) throw new Error('HTTP ' + response.status);
    projects = await response.json();
    renderFilters();
    renderProjects();
  }catch(error){
    console.error('Не удалось загрузить projects.json', error);
    grid.innerHTML = '<p class="loading">Не удалось загрузить список проектов. Обновите страницу или откройте репозиторий на GitHub.</p>';
  }
}
const menuButton = $('.menu-toggle');
const mobileNav = $('.mobile-nav');
menuButton.addEventListener('click', () => {
  const open = mobileNav.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
});
mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  mobileNav.classList.remove('open');
  menuButton.setAttribute('aria-expanded','false');
}));
$('#year').textContent = new Date().getFullYear();
init();