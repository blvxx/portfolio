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

function makePreview(project){
  const preview = project.preview;
  const shell = document.createElement('div');
  shell.className = 'project-preview';
  const toolbar = document.createElement('div');
  toolbar.className = 'preview-toolbar';
  const dots = document.createElement('span');
  dots.className = 'preview-dots';
  dots.textContent = '•••';
  const label = document.createElement('span');
  label.className = 'preview-address';
  label.textContent = preview?.type === 'iframe' ? new URL(preview.src).hostname + '/…' : (preview?.label || 'PROJECT SNAPSHOT');
  toolbar.append(dots,label);
  shell.appendChild(toolbar);

  if(preview?.type === 'iframe'){
    const frame = document.createElement('iframe');
    frame.className = 'preview-frame';
    frame.src = preview.src;
    frame.title = preview.alt || project.title + ' — live preview';
    frame.loading = 'lazy';
    frame.referrerPolicy = 'no-referrer';
    frame.setAttribute('sandbox','allow-scripts allow-forms');
    shell.appendChild(frame);
  }else if(preview?.type === 'image'){
    const image = document.createElement('img');
    image.className = 'preview-image';
    image.src = preview.src;
    image.alt = preview.alt || project.title;
    image.loading = 'lazy';
    shell.appendChild(image);
  }else{
    const artifact = document.createElement('div');
    artifact.className = 'artifact-preview';
    const eyebrow = document.createElement('span');
    eyebrow.className = 'artifact-label';
    eyebrow.textContent = preview?.label || 'PROJECT ARTIFACT';
    const heading = document.createElement('strong');
    heading.textContent = preview?.headline || project.title;
    const list = document.createElement('ul');
    (preview?.lines || []).forEach(line => {
      const item = document.createElement('li');
      item.textContent = line;
      list.appendChild(item);
    });
    const foot = document.createElement('span');
    foot.className = 'artifact-footer';
    foot.textContent = preview?.footer || project.tech.join(' · ');
    artifact.append(eyebrow,heading,list,foot);
    shell.appendChild(artifact);
  }
  return shell;
}
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
    card.appendChild(makePreview(project));
    const body = document.createElement('div');
    body.className = 'project-body';
    const kicker = document.createElement('span');
    kicker.className = 'project-kicker project-kicker-body';
    kicker.textContent = project.kicker;
    const title = document.createElement('h3');
    title.className = 'project-title';
    title.textContent = project.title;
    const description = document.createElement('p');
    description.className = 'project-description';
    description.textContent = project.description;
    body.append(kicker,title,description);
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
    const actions = document.createElement('div');
    actions.className = 'project-actions';
    if(project.demo_url){
      const demo = document.createElement('a');
      demo.className = 'project-link project-link-primary';
      demo.href = project.demo_url;
      demo.target = '_blank';
      demo.rel = 'noopener noreferrer';
      demo.textContent = (project.demo_label || 'Демо') + ' ↗';
      actions.appendChild(demo);
    }
    const link = document.createElement('a');
    link.className = 'project-link';
    link.href = project.url;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = (project.link || 'GitHub') + ' ↗';
    actions.appendChild(link);
    footer.append(status,actions);
    body.appendChild(footer);
    card.appendChild(body);
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