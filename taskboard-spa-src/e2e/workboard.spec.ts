import { expect, test, type Locator, type Page } from "@playwright/test";

const smokeTask = "QA smoke task";
const editedTask = "QA smoke task edited";

async function createTask(
  page: Page,
  title: string,
  options: { project?: string; priority?: string; status?: string } = {},
): Promise<void> {
  await page.getByRole("button", { name: /New task/ }).click();
  const dialog = page.getByRole("dialog");
  await expect(dialog).toBeVisible();
  await dialog.getByLabel(/Task title/).fill(title);
  await dialog.getByLabel("Project").selectOption(options.project ?? "Platform");
  await dialog.getByLabel("Priority").selectOption(options.priority ?? "high");
  await dialog.getByLabel("Status").selectOption(options.status ?? "backlog");
  await dialog.getByRole("button", { name: "Create task" }).click();
  await expect(dialog).toBeHidden();
}

function taskCard(page: Page, title: string): Locator {
  return page.locator(".task-card").filter({
    has: page.getByRole("button", { name: title, exact: true }),
  });
}

test("renders the demo workspace and four workflow columns", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Task board" })).toBeVisible();
  for (const name of ["Backlog", "In progress", "In review", "Done"]) {
    await expect(page.getByRole("heading", { name, exact: true })).toBeVisible();
  }
  await expect(page.locator(".task-card")).toHaveCount(6);
  await expect(page.getByText("Demo environment")).toBeVisible();
});

test("creates, searches, edits, advances, deletes and resets a task", async ({ page }) => {
  await page.goto("/");
  await createTask(page, smokeTask);

  await expect(taskCard(page, smokeTask)).toHaveCount(1);
  await page.getByRole("textbox", { name: "Search tasks, people or tags" }).fill("QA smoke");
  await expect(taskCard(page, smokeTask)).toHaveCount(1);
  await page.getByRole("textbox", { name: "Search tasks, people or tags" }).fill("");
  await expect(page.locator(".task-card")).toHaveCount(7);

  await taskCard(page, smokeTask).getByRole("button", { name: smokeTask }).click();
  const editDialog = page.getByRole("dialog");
  await expect(editDialog).toBeVisible();
  await editDialog.getByLabel(/Task title/).fill(editedTask);
  await editDialog.getByRole("button", { name: "Save changes" }).click();
  await expect(taskCard(page, editedTask)).toHaveCount(1);

  await taskCard(page, editedTask)
    .getByRole("button", { name: `Move task to next stage: ${editedTask}` })
    .click();
  const inProgressColumn = page
    .locator(".board-column")
    .filter({ has: page.getByRole("heading", { name: "In progress", exact: true }) });
  await expect(inProgressColumn.getByRole("button", { name: editedTask })).toHaveCount(1);

  await page.getByRole("button", { name: /List/ }).click();
  const editedRow = page.getByRole("row").filter({ hasText: editedTask });
  await expect(editedRow).toBeVisible();
  await expect(editedRow.getByText("In progress")).toBeVisible();

  await page.getByRole("button", { name: /Board/ }).click();
  await taskCard(page, editedTask).getByRole("button", { name: editedTask }).click();
  await page.getByRole("dialog").getByRole("button", { name: "Delete task" }).click();
  await expect(page.getByRole("button", { name: editedTask })).toHaveCount(0);

  await page.getByRole("button", { name: "Reset demo" }).click();
  await expect(page.locator(".task-card")).toHaveCount(6);
  await expect(page.getByRole("heading", { name: "Backlog", exact: true })).toBeVisible();
});

test("filters the list by project, priority and text", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /List/ }).click();

  await page.locator(".side-nav").getByRole("button", { name: /Growth/ }).click();
  await expect(page.locator("tbody tr")).toHaveCount(2);

  await page.getByLabel("Filter by priority").selectOption("low");
  await expect(page.locator("tbody tr")).toHaveCount(2);

  await page.getByRole("textbox", { name: "Search tasks, people or tags" }).fill("pricing");
  await expect(page.locator("tbody tr")).toHaveCount(1);
  await expect(page.locator("tbody")).toContainText("Refresh pricing page copy");

  await page.getByRole("button", { name: "Reset demo" }).click();
  await expect(page.locator("tbody tr")).toHaveCount(6);
});

test("persists new tasks after a browser reload", async ({ page }) => {
  await page.goto("/");
  await createTask(page, "Persistence check", { project: "Growth", priority: "medium" });
  await expect(taskCard(page, "Persistence check")).toHaveCount(1);
  await page.reload();
  await expect(taskCard(page, "Persistence check")).toHaveCount(1);
  await page.getByRole("button", { name: "Reset demo" }).click();
  await expect(page.locator(".task-card")).toHaveCount(6);
});

test("handles corrupt local storage and recovers the sample workspace", async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem("workboard-demo-v1", "{invalid-json");
  });
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Task board" })).toBeVisible();
  await expect(page.locator(".task-card")).toHaveCount(6);
});

test("keeps the workspace usable at a narrow mobile viewport", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Task board" })).toBeVisible();
  const dimensions = await page.evaluate(() => ({
    viewport: document.documentElement.clientWidth,
    content: document.documentElement.scrollWidth,
  }));
  expect(dimensions.content).toBeLessThanOrEqual(dimensions.viewport);
});
