export const TASK_STATUSES = ["backlog", "in-progress", "review", "done"] as const;
export type TaskStatus = (typeof TASK_STATUSES)[number];

export const TASK_PRIORITIES = ["urgent", "high", "medium", "low"] as const;
export type TaskPriority = (typeof TASK_PRIORITIES)[number];

export interface Task {
  id: string;
  title: string;
  description: string;
  project: string;
  assignee: string;
  status: TaskStatus;
  priority: TaskPriority;
  dueDate: string;
  tags: string[];
  createdAt: string;
}

export type TaskDraft = Omit<Task, "id" | "createdAt">;

export interface TaskFilters {
  query?: string;
  project?: string;
  priority?: TaskPriority | "all";
}

export interface TaskSummary {
  total: number;
  active: number;
  completed: number;
  urgent: number;
  inReview: number;
}

const validStatuses = new Set<string>(TASK_STATUSES);
const validPriorities = new Set<string>(TASK_PRIORITIES);

export function createTask(
  draft: TaskDraft,
  id: string,
  createdAt = new Date().toISOString(),
): Task {
  const title = draft.title.trim();
  if (!title) {
    throw new Error("A task title is required.");
  }

  return {
    ...draft,
    id,
    title,
    description: draft.description.trim(),
    project: draft.project.trim(),
    assignee: draft.assignee.trim(),
    tags: [...new Set(draft.tags.map((tag) => tag.trim()).filter(Boolean))],
    createdAt,
  };
}

export function updateTask(tasks: Task[], id: string, draft: TaskDraft): Task[] {
  return tasks.map((task) =>
    task.id === id ? createTask(draft, task.id, task.createdAt) : task,
  );
}

export function moveTask(tasks: Task[], id: string, status: TaskStatus): Task[] {
  return tasks.map((task) => (task.id === id ? { ...task, status } : task));
}

export function moveTaskForward(tasks: Task[], id: string): Task[] {
  const current = tasks.find((task) => task.id === id);
  if (!current) return tasks;
  const currentIndex = TASK_STATUSES.indexOf(current.status);
  const nextStatus = TASK_STATUSES[Math.min(currentIndex + 1, TASK_STATUSES.length - 1)] ?? current.status;
  return nextStatus === current.status ? tasks : moveTask(tasks, id, nextStatus);
}

export function reopenTask(tasks: Task[], id: string): Task[] {
  return moveTask(tasks, id, "backlog");
}

export function deleteTask(tasks: Task[], id: string): Task[] {
  return tasks.filter((task) => task.id !== id);
}

export function filterTasks(tasks: Task[], filters: TaskFilters = {}): Task[] {
  const query = filters.query?.trim().toLocaleLowerCase() ?? "";
  return tasks.filter((task) => {
    const matchesQuery =
      !query ||
      [task.title, task.description, task.project, task.assignee, ...task.tags]
        .join(" ")
        .toLocaleLowerCase()
        .includes(query);
    const matchesProject = !filters.project || filters.project === "all" || task.project === filters.project;
    const matchesPriority =
      !filters.priority || filters.priority === "all" || task.priority === filters.priority;
    return matchesQuery && matchesProject && matchesPriority;
  });
}

export function summarizeTasks(tasks: Task[]): TaskSummary {
  return {
    total: tasks.length,
    active: tasks.filter((task) => task.status !== "done").length,
    completed: tasks.filter((task) => task.status === "done").length,
    urgent: tasks.filter((task) => task.priority === "urgent" && task.status !== "done").length,
    inReview: tasks.filter((task) => task.status === "review").length,
  };
}

export function parseTasks(raw: string | null, fallback: Task[]): Task[] {
  if (!raw) return fallback;
  try {
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) return fallback;
    return parsed.filter(isTask);
  } catch {
    return fallback;
  }
}

function isTask(value: unknown): value is Task {
  if (!value || typeof value !== "object") return false;
  const task = value as Record<string, unknown>;
  return (
    typeof task.id === "string" &&
    typeof task.title === "string" &&
    typeof task.description === "string" &&
    typeof task.project === "string" &&
    typeof task.assignee === "string" &&
    typeof task.status === "string" &&
    validStatuses.has(task.status) &&
    typeof task.priority === "string" &&
    validPriorities.has(task.priority) &&
    typeof task.dueDate === "string" &&
    Array.isArray(task.tags) &&
    task.tags.every((tag) => typeof tag === "string") &&
    typeof task.createdAt === "string"
  );
}
