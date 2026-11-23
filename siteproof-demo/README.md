# SiteProof — WordPress form diagnostic prototype

A public, interactive portfolio demonstration of a manual-first workflow for checking a WordPress Contact Form 7 enquiry path.

**[Open the service page](./index.html)** · **[Open the interactive demo](./demo.html)** · **[Open the local diagnostic workspace](./workspace.html)**

## What this demonstrates

- A structured workflow for a single authorised form.
- Separate evidence stages: page/form present, test submission accepted, message generated and email actually received.
- A sample operator dashboard with synthetic sample records.
- A local-first workspace for recording a manually performed diagnostic and exporting a report.
- Clear scoping, limitations and customer-safety rules.

## Important: prototype boundaries

This is a static portfolio prototype. It does **not** contact external websites, submit WordPress forms, send email, verify mailbox delivery, run background monitoring or store data on a server. The demo dashboard uses synthetic records. The workspace saves operator-entered demo records in the current browser's localStorage only; data is local to that browser and can be lost when browser storage is cleared.

Do not enter real customer submissions, personal data, credentials, passwords, API tokens or mailbox details. Do not test a website without explicit permission and an agreed safe test route.

## Service concept

The landing page describes a proposed manual diagnostic of one WordPress Contact Form 7 form. The illustrative offer is 1,000 ₽; the page opens an email draft to the public contact address. This repository does not accept payments or create real bookings. The service is not an automatic SaaS and does not guarantee future email delivery.

## Run locally

No build tools are required. Open `index.html` in a browser. The interactive workspace is browser-local and does not make network requests.

## Source and status

Copied as a public product showcase from a separate private prototype. Internal prospect lists, sales pipelines, outreach drafts, operating notes and private commercial material are intentionally not included. This public showcase documents only the product UI and its verified limits.
