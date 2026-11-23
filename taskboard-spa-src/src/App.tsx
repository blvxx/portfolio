import { useCallback, useEffect, useMemo, useRef, useState, type FormEvent } from "react";
import {
  createTask,
  deleteTask,
  filterTasks,
  moveTaskForward,
  parseTasks,
  reopenTask,
  summarizeTasks,
  updateTask,
  type Task,
  type TaskDraft,
  type TaskPriority,
  type TaskStatus,
} from "./domain";

const STORAGE_KEY = "workboard-demo-v1";
const projects = [
  { name: "Platform", color: "violet", icon: "◈" },
  { name: "Product", color: "blue", icon: "◇" },
  { name: "Growth", color: "orange", icon: "↗" },
];
const statuses: { id: TaskStatus; label: string; short: string; color: string }[] = [
  { id: "backlog", label: "Backlog", short: "To do", color: "slate" },
  { id: "in-progress", label: "In progress", short: "Active", color: "blue" },
  { id: "review", label: "In review", short: "Review", color: "violet" },
  { id: "done", label: "Done", short: "Complete", color: "green" },
];
const priorityLabels: Record<TaskPriority, string> = {
  urgent: "Urgent",
  high: "High",
  medium: "Medium",
  low: "Low",
};
const priorityOrder: TaskPriority[] = ["urgent", "high", "medium", "low"];

function dateOffset(days: number): string {
  const date = new Date();
  date.setDate(date.getDate() + days);
  return date.toISOString().slice(0, 10);
}

const seedTasks: Task[] = [
  {
    id: "WB-101",
    title: "Map the first-time user journey",
    description: "Review the onboarding steps and flag friction before the next product review.",
    project: "Product",
    assignee: "Alex Rivera",
    status: "in-progress",
    priority: "high",
    dueDate: dateOffset(2),
    tags: ["Research", "UX"],
    createdAt: "2026-11-18T09:30:00.000Z",
  },
  {
    id: "WB-102",
    title: "Investigate webhook retry behavior",
    description: "Verify retry boundaries and document the expected idempotency behavior.",
    project: "Platform",
    assignee: "Morgan Lee",
    status: "backlog",
    priority: "urgent",
    dueDate: dateOffset(1),
    tags: ["API", "Reliability"],
    createdAt: "2026-11-19T11:00:00.000Z",
  },
  {
    id: "WB-103",
    title: "Prepare release checklist",
    description: "Collect the sign-off items for the next staged release.",
    project: "Platform",
    assignee: "Jamie Chen",
    status: "review",
    priority: "medium",
    dueDate: dateOffset(4),
    tags: ["Release"],
    createdAt: "2026-11-19T14:15:00.000Z",
  },
  {
    id: "WB-104",
    title: "Refresh pricing page copy",
    description: "Align plan descriptions and clarify the free evaluation limits.",
    project: "Growth",
    assignee: "Taylor Brooks",
    status: "done",
    priority: "low",
    dueDate: dateOffset(-1),
    tags: ["Content", "Website"],
    createdAt: "2026-11-16T08:20:00.000Z",
  },
  {
    id: "WB-105",
    title: "Add keyboard navigation to filters",
    description: "Check focus order and visible focus styles in the board toolbar.",
    project: "Product",
    assignee: "Alex Rivera",
    status: "in-progress",
    priority: "medium",
    dueDate: dateOffset(5),
    tags: ["Accessibility", "Frontend"],
    createdAt: "2026-11-20T10:40:00.000Z",
  },
  {
    id: "WB-106",
    title: "Review usage event taxonomy",
    description: "Confirm event names and required properties with the analytics owner.",
    project: "Growth",
    assignee: "Morgan Lee",
    status: "backlog",
    priority: "low",
    dueDate: dateOffset(8),
    tags: ["Analytics"],
    createdAt: "2026-11-21T13:05:00.000Z",
  },
];

const emptyDraft = (): TaskDraft => ({
  title: "",
  description: "",
  project: "Product",
  assignee: "Alex Rivera",
  status: "backlog",
  priority: "medium",
  dueDate: dateOffset(3),
  tags: [],
});

function loadTasks(): Task[] {
  try {
    return parseTasks(localStorage.getItem(STORAGE_KEY), seedTasks);
  } catch {
    return seedTasks;
  }
}

function initials(name: string): string {
  return name
    .split(" ")
    .map((part) => part[0] ?? "")
    .join("")
    .slice(0, 2)
    .toUpperCase();
}

function formatDate(value: string): string {
  if (!value) return "No due date";
  const date = new Date(`${value}T12:00:00`);
  if (Number.isNaN(date.getTime())) return "No due date";
  return new Intl.DateTimeFormat("en", { month: "short", day: "numeric" }).format(date);
}

function dueDateClass(value: string): string {
  if (!value) return "due-date";
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const due = new Date(`${value}T00:00:00`);
  const diff = Math.round((due.getTime() - today.getTime()) / 86_400_000);
  if (diff < 0) return "due-date overdue";
  if (diff <= 1) return "due-date due-soon";
  return "due-date";
}

function displayId(id: string): string {
  return id.startsWith("WB-") ? id : `WB-${id.slice(-4).toUpperCase()}`;
}

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onAdvance: (task: Task) => void;
}

function TaskCard({ task, onEdit, onAdvance }: TaskCardProps) {
  const nextAction = task.status === "done" ? "Reopen task" : "Move task to next stage";
  return (
    <article className="task-card">
      <div className="task-card-top">
        <span className="task-id">{displayId(task.id)}</span>
        <span className={`priority-pill priority-${task.priority}`}>
          <span aria-hidden="true" />{priorityLabels[task.priority]}
        </span>
      </div>
      <h3 className="task-title-heading">
        <button type="button" onClick={() => onEdit(task)}>{task.title}</button>
      </h3>
      <p className="task-description">{task.description}</p>
      <div className="task-tags">
        {task.tags.slice(0, 3).map((tag) => <span key={tag}>{tag}</span>)}
      </div>
      <div className="task-card-footer">
        <div className="assignee" title={task.assignee}>
          <span className={`avatar avatar-${task.assignee.length % 4}`} aria-hidden="true">{initials(task.assignee)}</span>
          <span>{task.assignee.split(" ")[0]}</span>
        </div>
        <span className={dueDateClass(task.dueDate)} title={`Due ${formatDate(task.dueDate)}`}>
          <span aria-hidden="true">◷</span>{formatDate(task.dueDate)}
        </span>
      </div>
      <div className="task-card-actions">
        <span className="project-chip">{task.project}</span>
        <div className="task-action-group">
          <button className="icon-button" type="button" aria-label={`Edit ${task.title}`} onClick={() => onEdit(task)}>✎</button>
          <button className="advance-button" type="button" aria-label={`${nextAction}: ${task.title}`} onClick={() => onAdvance(task)}>
            {task.status === "done" ? "↶" : "→"}
          </button>
        </div>
      </div>
    </article>
  );
}

interface TaskModalProps {
  task: Task | null;
  draft: TaskDraft;
  setDraft: (draft: TaskDraft) => void;
  onClose: () => void;
  onSave: (event: FormEvent<HTMLFormElement>) => void;
  onDelete?: () => void;
}

function TaskModal({ task, draft, setDraft, onClose, onSave, onDelete }: TaskModalProps) {
  const dialogRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    const getFocusable = () =>
      Array.from(
        dialog?.querySelectorAll<HTMLElement>(
          'button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])',
        ) ?? [],
      ).filter((element) => element.offsetParent !== null);

    (dialog?.querySelector<HTMLElement>("[autofocus]") ?? getFocusable()[0])?.focus();

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        onClose();
        return;
      }
      if (event.key !== "Tab") return;
      const focusable = getFocusable();
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last?.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first?.focus();
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  const update = <K extends keyof TaskDraft>(key: K, value: TaskDraft[K]) => {
    setDraft({ ...draft, [key]: value });
  };

  return (
    <div className="modal-backdrop" onMouseDown={(event) => {
      if (event.target === event.currentTarget) onClose();
    }}>
      <section ref={dialogRef} className="task-modal" role="dialog" aria-modal="true" aria-labelledby="task-modal-title" aria-describedby="task-modal-description">
        <div className="modal-heading">
          <div>
            <span className="eyebrow">{task ? "TASK DETAILS" : "NEW WORK ITEM"}</span>
            <h2 id="task-modal-title">{task ? "Edit task" : "Create a task"}</h2>
            <p id="task-modal-description" className="modal-description">Keep the task details, owner and next step up to date.</p>
          </div>
          <button className="icon-button modal-close" type="button" onClick={onClose} aria-label="Close dialog">×</button>
        </div>
        <form onSubmit={onSave}>
          <label className="field full-field">
            <span>Task title <b aria-hidden="true">*</b></span>
            <input autoFocus required maxLength={100} value={draft.title} onChange={(event) => update("title", event.target.value)} placeholder="e.g. Review account recovery flow" />
          </label>
          <label className="field full-field">
            <span>Description</span>
            <textarea rows={3} maxLength={400} value={draft.description} onChange={(event) => update("description", event.target.value)} placeholder="Add context, acceptance criteria or next steps..." />
          </label>
          <div className="field-grid">
            <label className="field">
              <span>Project</span>
              <select value={draft.project} onChange={(event) => update("project", event.target.value)}>
                {projects.map((project) => <option key={project.name}>{project.name}</option>)}
              </select>
            </label>
            <label className="field">
              <span>Assignee</span>
              <select value={draft.assignee} onChange={(event) => update("assignee", event.target.value)}>
                {["Alex Rivera", "Morgan Lee", "Jamie Chen", "Taylor Brooks"].map((person) => <option key={person}>{person}</option>)}
              </select>
            </label>
            <label className="field">
              <span>Priority</span>
              <select value={draft.priority} onChange={(event) => update("priority", event.target.value as TaskPriority)}>
                {priorityOrder.map((priority) => <option key={priority} value={priority}>{priorityLabels[priority]}</option>)}
              </select>
            </label>
            <label className="field">
              <span>Status</span>
              <select value={draft.status} onChange={(event) => update("status", event.target.value as TaskStatus)}>
                {statuses.map((status) => <option key={status.id} value={status.id}>{status.label}</option>)}
              </select>
            </label>
            <label className="field">
              <span>Due date</span>
              <input type="date" value={draft.dueDate} onChange={(event) => update("dueDate", event.target.value)} />
            </label>
            <label className="field">
              <span>Tags <small>comma separated</small></span>
              <input value={draft.tags.join(", ")} onChange={(event) => update("tags", event.target.value.split(",").map((tag) => tag.trim()).filter(Boolean))} placeholder="API, UX, Release" />
            </label>
          </div>
          <div className="modal-footer">
            {task && onDelete ? <button className="text-danger" type="button" onClick={onDelete}>Delete task</button> : <span className="modal-note">Fields marked * are required.</span>}
            <div className="modal-buttons">
              <button className="button button-secondary" type="button" onClick={onClose}>Cancel</button>
              <button className="button button-primary" type="submit">{task ? "Save changes" : "Create task"}</button>
            </div>
          </div>
        </form>
      </section>
    </div>
  );
}

export default function App() {
  const [tasks, setTasks] = useState<Task[]>(loadTasks);
  const [query, setQuery] = useState("");
  const [projectFilter, setProjectFilter] = useState("all");
  const [priorityFilter, setPriorityFilter] = useState<TaskPriority | "all">("all");
  const [view, setView] = useState<"board" | "list">("board");
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [draft, setDraft] = useState<TaskDraft>(emptyDraft);
  const [notice, setNotice] = useState("");
  const searchInputRef = useRef<HTMLInputElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const onShortcut = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        searchInputRef.current?.focus();
      }
    };
    window.addEventListener("keydown", onShortcut);
    return () => window.removeEventListener("keydown", onShortcut);
  }, []);

  useEffect(() => {
    if (!isModalOpen) previousFocusRef.current?.focus();
  }, [isModalOpen]);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
    } catch {
      setNotice("Browser storage is unavailable. Changes will not persist after refresh.");
    }
  }, [tasks]);

  const visibleTasks = useMemo(
    () => filterTasks(tasks, { query, project: projectFilter, priority: priorityFilter }),
    [tasks, query, projectFilter, priorityFilter],
  );
  const summary = useMemo(() => summarizeTasks(tasks), [tasks]);

  const rememberFocus = () => {
    previousFocusRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
  };

  const openNewTask = () => {
    rememberFocus();
    setEditingTask(null);
    setDraft(emptyDraft());
    setIsModalOpen(true);
  };

  const openEditTask = (task: Task) => {
    rememberFocus();
    setEditingTask(task);
    setDraft({
      title: task.title,
      description: task.description,
      project: task.project,
      assignee: task.assignee,
      status: task.status,
      priority: task.priority,
      dueDate: task.dueDate,
      tags: [...task.tags],
    });
    setIsModalOpen(true);
  };

  const closeModal = useCallback(() => setIsModalOpen(false), []);

  const saveTask = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      if (editingTask) {
        setTasks((current) => updateTask(current, editingTask.id, draft));
        setNotice("Task updated successfully.");
      } else {
        const uuid = globalThis.crypto?.randomUUID?.();
        const newId = `WB-${(uuid ?? Date.now().toString(36)).replaceAll("-", "").slice(0, 12).toUpperCase()}`;
        const created = createTask(draft, newId);
        setTasks((current) => [created, ...current]);
        setNotice("New task added to the workspace.");
      }
      setIsModalOpen(false);
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Unable to save this task.");
    }
  };

  const removeTask = () => {
    if (!editingTask) return;
    setTasks((current) => deleteTask(current, editingTask.id));
    setIsModalOpen(false);
    setNotice("Task deleted.");
  };

  const advanceTask = (task: Task) => {
    if (task.status === "done") {
      setTasks((current) => reopenTask(current, task.id));
      setNotice(`${displayId(task.id)} moved back to Backlog.`);
    } else {
      setTasks((current) => moveTaskForward(current, task.id));
      setNotice(`${displayId(task.id)} moved to the next stage.`);
    }
  };

  const exportTasks = () => {
    const blob = new Blob([JSON.stringify({ exportedAt: new Date().toISOString(), tasks }, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "workboard-tasks.json";
    anchor.click();
    URL.revokeObjectURL(url);
    setNotice("Task data exported as JSON.");
  };

  const resetDemo = () => {
    setTasks(seedTasks);
    setQuery("");
    setProjectFilter("all");
    setPriorityFilter("all");
    setNotice("Demo workspace restored.");
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#overview" aria-label="Workboard overview">
          <span className="brand-mark">W</span>
          <span><strong>workboard</strong><small>TEAM WORKSPACE</small></span>
        </a>

        <div className="workspace-switcher">
          <span className="workspace-avatar">AC</span>
          <span className="workspace-label"><strong>Acme Creative</strong><small>Free demo workspace</small></span>
          <span className="switcher-arrow" aria-hidden="true">⌄</span>
        </div>

        <nav className="side-nav" aria-label="Main navigation">
          <span className="nav-caption">WORKSPACE</span>
          <a className="nav-link active" href="#overview"><span>▦</span> Overview</a>
          <a className="nav-link" href="#board"><span>▤</span> Task board <em>{tasks.length}</em></a>
          <a className="nav-link" href="#projects"><span>◫</span> Projects</a>
          <span className="nav-caption nav-caption-spaced">PROJECTS</span>
          <button className={`project-link ${projectFilter === "all" ? "selected" : ""}`} type="button" onClick={() => setProjectFilter("all")}>
            <span className="project-dot all-dot" />All projects <small>{tasks.length}</small>
          </button>
          {projects.map((project) => (
            <button className={`project-link ${projectFilter === project.name ? "selected" : ""}`} type="button" key={project.name} onClick={() => setProjectFilter(project.name)}>
              <span className={`project-dot ${project.color}-dot`} />{project.name}
              <small>{tasks.filter((task) => task.project === project.name).length}</small>
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="upgrade-card">
            <span className="upgrade-icon">✦</span>
            <strong>Keep the work moving</strong>
            <p>This workspace is a local-first product demo. Your changes stay in this browser.</p>
            <a href="https://github.com/blvxx/portfolio/tree/main/taskboard-spa-src" target="_blank" rel="noreferrer">Explore the build ↗</a>
          </div>
          <div className="profile-row">
            <span className="avatar avatar-profile">AR</span>
            <span><strong>Alex Rivera</strong><small>Workspace admin</small></span>
            <span className="profile-more" aria-hidden="true">···</span>
          </div>
        </div>
      </aside>

      <main className="main-content" id="overview">
        <header className="topbar">
          <div className="breadcrumbs"><span>Workspace</span><b>/</b><strong>Overview</strong></div>
          <div className="topbar-right">
            <span className="demo-status"><i /> Demo environment</span>
            <button className="topbar-icon" type="button" onClick={exportTasks} aria-label="Export task data">⇩</button>
            <span className="avatar avatar-profile">AR</span>
          </div>
        </header>

        <div className="content-wrap">
          <section className="page-heading">
            <div>
              <div className="eyebrow">MONDAY · PROJECT OVERVIEW</div>
              <h1>Good morning, Alex <span>✦</span></h1>
              <p>Here’s what’s happening across your projects today.</p>
            </div>
            <div className="heading-actions">
              <button className="button button-secondary" type="button" onClick={resetDemo}>↻ Reset demo</button>
              <button className="button button-primary" type="button" onClick={openNewTask}><span>＋</span> New task</button>
            </div>
          </section>

          <section className="stats-grid" aria-label="Workspace summary">
            <article className="stat-card">
              <div className="stat-top"><span>Total tasks</span><span className="stat-icon indigo">▤</span></div>
              <strong>{summary.total.toString().padStart(2, "0")}</strong>
              <small><span className="trend-up">↑</span> Across all projects</small>
            </article>
            <article className="stat-card">
              <div className="stat-top"><span>In progress</span><span className="stat-icon blue">◴</span></div>
              <strong>{summary.active.toString().padStart(2, "0")}</strong>
              <small>Tasks not yet completed</small>
            </article>
            <article className="stat-card">
              <div className="stat-top"><span>In review</span><span className="stat-icon violet">◉</span></div>
              <strong>{summary.inReview.toString().padStart(2, "0")}</strong>
              <small>Waiting for feedback</small>
            </article>
            <article className="stat-card">
              <div className="stat-top"><span>Urgent priority</span><span className="stat-icon orange">⚑</span></div>
              <strong>{summary.urgent.toString().padStart(2, "0")}</strong>
              <small>Needs attention first</small>
            </article>
          </section>

          <section className="board-section" id="board">
            <div className="board-heading">
              <div>
                <div className="section-title-row"><h2>Task board</h2><span className="total-pill">{visibleTasks.length} tasks</span></div>
                <p>Track work from backlog to completion.</p>
              </div>
              <div className="view-toggle" role="group" aria-label="Choose task view">
                <button className={view === "board" ? "active" : ""} type="button" onClick={() => setView("board")} aria-pressed={view === "board"}>▦ Board</button>
                <button className={view === "list" ? "active" : ""} type="button" onClick={() => setView("list")} aria-pressed={view === "list"}>☷ List</button>
              </div>
            </div>

            <div className="toolbar">
              <label className="search-box">
                <span aria-hidden="true">⌕</span>
                <input ref={searchInputRef} value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search tasks, people or tags..." aria-label="Search tasks, people or tags" />
                <kbd>⌘ K</kbd>
              </label>
              <label className="filter-select">
                <span className="sr-only">Filter by priority</span>
                <select value={priorityFilter} onChange={(event) => setPriorityFilter(event.target.value as TaskPriority | "all")}>
                  <option value="all">All priorities</option>
                  {priorityOrder.map((priority) => <option key={priority} value={priority}>{priorityLabels[priority]}</option>)}
                </select>
              </label>
              <button className="toolbar-button" type="button" onClick={exportTasks}>⇩ <span>Export</span></button>
            </div>

            {view === "board" ? (
              <div className="board-grid">
                {statuses.map((status) => {
                  const columnTasks = visibleTasks.filter((task) => task.status === status.id);
                  return (
                    <section className="board-column" key={status.id} aria-labelledby={`column-${status.id}`}>
                      <div className="column-heading">
                        <div><span className={`column-indicator ${status.color}`} /><h3 id={`column-${status.id}`}>{status.label}</h3><span className="column-count">{columnTasks.length}</span></div>
                        <button className="column-menu" type="button" aria-label={`Create a task in ${status.label}`} onClick={() => {
                          setEditingTask(null);
                          setDraft({ ...emptyDraft(), status: status.id, project: projectFilter === "all" ? "Product" : projectFilter });
                          setIsModalOpen(true);
                        }}>＋</button>
                      </div>
                      <div className="column-cards">
                        {columnTasks.length ? columnTasks.map((task) => (
                          <TaskCard key={task.id} task={task} onEdit={openEditTask} onAdvance={advanceTask} />
                        )) : <div className="empty-column">No tasks here yet</div>}
                      </div>
                    </section>
                  );
                })}
              </div>
            ) : (
              <div className="list-panel">
                <table>
                  <thead><tr><th>Task</th><th>Project</th><th>Assignee</th><th>Priority</th><th>Status</th><th>Due date</th><th><span className="sr-only">Actions</span></th></tr></thead>
                  <tbody>
                    {visibleTasks.map((task) => (
                      <tr key={task.id}>
                        <td><button className="table-task" type="button" onClick={() => openEditTask(task)}>{task.title}<small>{displayId(task.id)}</small></button></td>
                        <td>{task.project}</td>
                        <td><span className="table-assignee"><span className="avatar avatar-tiny">{initials(task.assignee)}</span>{task.assignee}</span></td>
                        <td><span className={`priority-pill priority-${task.priority}`}><span aria-hidden="true" />{priorityLabels[task.priority]}</span></td>
                        <td><span className={`status-pill status-${task.status}`}>{statuses.find((status) => status.id === task.status)?.label}</span></td>
                        <td>{formatDate(task.dueDate)}</td>
                        <td><button className="icon-button" type="button" aria-label={`Edit ${task.title}`} onClick={() => openEditTask(task)}>✎</button></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {!visibleTasks.length && <div className="empty-list">No tasks match these filters.</div>}
              </div>
            )}
          </section>

          <section className="bottom-grid" id="projects">
            <article className="info-panel">
              <div className="info-panel-heading"><div><span className="eyebrow">PROJECT HEALTH</span><h2>Work by project</h2></div><span className="panel-icon">◫</span></div>
              <div className="project-health-list">
                {projects.map((project) => {
                  const projectTasks = tasks.filter((task) => task.project === project.name);
                  const completed = projectTasks.filter((task) => task.status === "done").length;
                  const percent = projectTasks.length ? Math.round((completed / projectTasks.length) * 100) : 0;
                  return (
                    <button className="health-row" type="button" key={project.name} onClick={() => setProjectFilter(project.name)}>
                      <span className={`project-dot ${project.color}-dot`} />
                      <span className="health-name">{project.name}<small>{completed} of {projectTasks.length} completed</small></span>
                      <span className="progress-track"><span style={{ width: `${percent}%` }} /></span>
                      <strong>{percent}%</strong>
                    </button>
                  );
                })}
              </div>
            </article>
            <article className="info-panel priority-panel">
              <div className="info-panel-heading"><div><span className="eyebrow">FOCUS FOR TODAY</span><h2>Priority snapshot</h2></div><span className="panel-icon">✦</span></div>
              <div className="focus-list">
                {tasks.filter((task) => task.priority === "urgent" && task.status !== "done").slice(0, 3).map((task) => (
                  <button type="button" className="focus-task" key={task.id} onClick={() => openEditTask(task)}>
                    <span className="focus-flag">!</span><span>{task.title}<small>{task.project} · {displayId(task.id)}</small></span><b>→</b>
                  </button>
                ))}
                {!summary.urgent && <p className="focus-empty">No urgent tasks at the moment. Nice work.</p>}
              </div>
            </article>
          </section>

          <footer className="page-footer">
            <span>Workboard demo · React + TypeScript</span>
            <span><a href="https://github.com/blvxx/portfolio/tree/main/taskboard-spa-src" target="_blank" rel="noreferrer">Source code ↗</a><i /> Local browser storage only</span>
          </footer>
        </div>
      </main>

      {notice && <div className="notice" role="status" aria-live="polite">{notice}<button type="button" aria-label="Dismiss notification" onClick={() => setNotice("")}>×</button></div>}
      {isModalOpen && (
        <TaskModal
          task={editingTask}
          draft={draft}
          setDraft={setDraft}
          onClose={closeModal}
          onSave={saveTask}
          onDelete={editingTask ? removeTask : undefined}
        />
      )}
    </div>
  );
}
