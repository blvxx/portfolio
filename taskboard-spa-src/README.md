# Workboard — React + TypeScript Task Management SPA

A responsive single-page task and project management interface built as a frontend engineering case study for an internal team workspace.

**[Open the live demo](https://blvxx.github.io/portfolio/taskboard-spa/)** · **[Open the source](https://github.com/blvxx/portfolio/tree/main/taskboard-spa-src)**

## Product scope

Workboard demonstrates a small project-management workflow without a backend:

- Four workflow stages: Backlog, In progress, In review and Done.
- Create, edit, delete and advance tasks between workflow stages.
- Project, assignee, priority, due date and tags on each task.
- Combined search, project selection and priority filtering.
- Board and table/list views.
- Summary cards, per-project completion progress and urgent-task snapshot.
- Browser-local persistence with defensive JSON parsing.
- JSON export of the current workspace.
- Responsive layout, semantic controls, visible focus, modal Escape handling and a keyboard shortcut (Ctrl/Cmd + K) for search.

## Architecture

- **React** owns interactive UI state and component composition.
- **TypeScript** defines task, status, priority, form and filter contracts.
- `src/domain.ts` contains pure task operations, validation, selectors, summary calculations and storage parsing.
- `src/App.tsx` composes the workspace, board/list views and task editor.
- `src/domain.test.ts` covers domain behavior with Vitest.
- `e2e/workboard.spec.ts` covers six Chromium browser flows: initial render, task lifecycle, filters, persistence, corrupt storage recovery and mobile overflow.
- Vite builds a static bundle under `dist/`; GitHub Actions publishes the generated files to the sibling `taskboard-spa/` directory for GitHub Pages.

The task domain is deliberately separated from the UI so validation, transitions and filtering can be tested without a browser or network.

## Local development

Requirements: Node.js 22.12+ and npm.

```bash
npm install
npm run dev
```

Quality checks:

```bash
npm run typecheck
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

## Verification

The GitHub Actions workflow runs strict TypeScript checks, Vitest domain tests, a production Vite build and six Chromium Playwright E2E scenarios. It uploads browser traces on failure. On pushes to `main`, it publishes the generated static site to:

`https://blvxx.github.io/portfolio/taskboard-spa/`

The demo is a static frontend only. It has no authentication, API, server-side database, collaboration, real notification service or permission model. Tasks are saved in the current browser's localStorage and should be treated as synthetic demo data. Do not enter real customer, employee or confidential business information.

## Product decisions and limitations

- A single browser profile is the source of truth; there is no cross-device or multi-user sync.
- Sample projects, team members and tasks are fictional.
- The JSON export is a convenience backup, not an encrypted or managed backup.
- Status moves are explicit UI actions; there is no drag-and-drop dependency.
- Authentication, role-based access, API persistence, audit history, real-time collaboration and server validation are intentionally outside this frontend-only case study.

## Maintainer

Artem Kalinin · [GitHub](https://github.com/blvxx)
