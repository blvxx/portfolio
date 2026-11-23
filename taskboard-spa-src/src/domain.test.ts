import { describe, expect, it } from "vitest";
import {
  createTask,
  deleteTask,
  filterTasks,
  moveTask,
  moveTaskForward,
  parseTasks,
  reopenTask,
  summarizeTasks,
  updateTask,
  type Task,
  type TaskDraft,
} from "./domain";

const draft: TaskDraft = {
  title: "  Review onboarding flow  ",
  description: " Check empty, loading and error states. ",
  project: "Platform",
  assignee: "Alex Rivera",
  status: "backlog",
  priority: "high",
  dueDate: "2026-12-02",
  tags: ["UX", "frontend", "UX"],
};

const fixtures: Task[] = [
  createTask({ ...draft, id: undefined as never }, "WB-101", "2026-11-20T10:00:00.000Z"),
  createTask(
    { ...draft, title: "Investigate webhook retries", status: "in-progress", priority: "urgent", project: "Platform" },
    "WB-102",
    "2026-11-21T10:00:00.000Z",
  ),
  createTask(
    { ...draft, title: "Prepare release notes", status: "review", priority: "medium", project: "Growth" },
    "WB-103",
    "2026-11-22T10:00:00.000Z",
  ),
  createTask(
    { ...draft, title: "Publish Q4 checklist", status: "done", priority: "low", project: "Growth" },
    "WB-104",
    "2026-11-23T10:00:00.000Z",
  ),
];

describe("task domain", () => {
  it("normalises task input and removes duplicate tags", () => {
    const task = createTask(draft, "WB-200", "2026-11-23T12:00:00.000Z");
    expect(task.title).toBe("Review onboarding flow");
    expect(task.description).toBe("Check empty, loading and error states.");
    expect(task.tags).toEqual(["UX", "frontend"]);
  });

  it("rejects a blank task title", () => {
    expect(() => createTask({ ...draft, title: "  " }, "WB-201")).toThrow(
      "A task title is required.",
    );
  });

  it("updates an existing task without changing its identity", () => {
    const updated = updateTask(fixtures, "WB-101", { ...draft, title: "Updated onboarding" });
    expect(updated[0]?.title).toBe("Updated onboarding");
    expect(updated[0]?.id).toBe("WB-101");
    expect(updated[1]?.title).toBe("Investigate webhook retries");
  });

  it("moves a task to a selected status", () => {
    const moved = moveTask(fixtures, "WB-101", "review");
    expect(moved[0]?.status).toBe("review");
  });

  it("moves tasks forward one stage and leaves Done unchanged", () => {
    expect(moveTaskForward(fixtures, "WB-101")[0]?.status).toBe("in-progress");
    expect(moveTaskForward(fixtures, "WB-104")).toEqual(fixtures);
  });

  it("reopens a completed task into Backlog", () => {
    expect(reopenTask(fixtures, "WB-104")[3]?.status).toBe("backlog");
  });

  it("deletes only the selected task", () => {
    const remaining = deleteTask(fixtures, "WB-102");
    expect(remaining).toHaveLength(3);
    expect(remaining.some((task) => task.id === "WB-102")).toBe(false);
  });

  it("combines free-text, project and priority filters", () => {
    const found = filterTasks(fixtures, { query: "webhook", project: "Platform", priority: "urgent" });
    expect(found.map((task) => task.id)).toEqual(["WB-102"]);
  });

  it("summarises status and priority counts", () => {
    expect(summarizeTasks(fixtures)).toEqual({
      total: 4,
      active: 3,
      completed: 1,
      urgent: 1,
      inReview: 1,
    });
  });

  it("uses fallback data for malformed persisted JSON", () => {
    expect(parseTasks("{broken", fixtures)).toEqual(fixtures);
  });

  it("filters invalid records from persisted JSON", () => {
    const raw = JSON.stringify([fixtures[0], { id: "bad", title: "missing fields" }]);
    expect(parseTasks(raw, fixtures)).toEqual([fixtures[0]]);
  });
});
