# Games Support Cases

All scenarios below are fictional and intended for interview practice.

## GS-001 — Purchase not credited

**Player message**

> I bought 1,000 coins. The payment went through, but my balance hasn't changed. I restarted the game twice.

**Simulated priority:** P2 for one player; raise to P1 if monitoring or multiple tickets show a wider payment-delivery incident.

**First response (EN)**

> Hi! Thanks for letting us know. I understand how frustrating it is when a purchase is charged but the in-game balance doesn't update. I'll help check the transaction. Please share the platform/store, approximate purchase time with timezone, and the order or transaction reference from the store receipt. Please don't send full card details, passwords or verification codes.

**Safe triage**

1. Confirm the game account using the approved verification method; do not ask for credentials.
2. Capture platform/store, region, approximate UTC time, order reference, product SKU and game account ID through approved support tooling.
3. Check known payment incidents and store transaction status.
4. Compare provider transaction, entitlement grant and current in-game balance. Look for pending, failed, duplicated or delayed events.
5. Do not grant currency manually or promise a refund unless the authorised payment process permits it.

**Decision**

- Store payment is pending: explain that the store has not confirmed completion and provide the approved next step.
- Payment is confirmed but entitlement is missing: escalate to Billing / Backend with the transaction reference and timestamps.
- Entitlement is granted but balance display is stale: route to the game/client team with build, platform and reproduction evidence.
- Several users are affected: link reports to an incident and notify the incident owner.

**Internal note**

`Player reports charged purchase / missing currency. Platform: [value]. Order ref: [redacted/reference]. Purchase time: [UTC]. Store state: [verified state]. Entitlement state: [verified state]. Scope: [single/multiple]. Next owner: [team]. Next update due: [time].`

## GS-002 — Suspected account compromise

**Player message**

> Someone logged into my account and changed the email. I can't get in. Please tell me how to get it back.

**Simulated priority:** P1 security-sensitive account incident.

**First response (EN)**

> I'm sorry this happened. Account security is the priority. Please stop sharing account details in public chats and use our official account-recovery route. I won't ask you for your password or one-time codes. I'll route this to the account-security team and keep the case restricted to the approved recovery process.

**Safe triage**

1. Use the approved ownership-verification workflow only.
2. Record the last known successful access time, platform, approximate location/region and whether the player still controls the registered recovery channel.
3. Check whether the account has an active security incident or recent recovery changes, if support tooling permits.
4. Preserve relevant audit references; do not expose them to the player.
5. Follow the security team's containment instructions. Do not independently change email, reset credentials or disable protections outside permissions.

**Escalation**

Immediate handoff to Account Security. Include verified account reference, reported time window, changes described by the player, verification status and any known linked reports. Do not place sensitive account data in general chat or broad team channels.

## GS-003 — Cannot log in after update

**Player message**

> Since today's update the game closes on the loading screen. I can't get past 20%.

**Simulated priority:** P2 if the player is blocked; P1 if a release-related pattern affects many players.

**First response (EN)**

> Thanks for the details. Let's narrow down whether this is related to the latest build or your device. Which platform and device model are you using, what game version is shown, and approximately when did the issue start? Please share the error text or a screenshot with personal information hidden.

**Triage checklist**

- Compare the build number with the release timeline and known-issues feed.
- Capture OS/device model, platform, region, network type, error code and timestamp/timezone.
- Ask whether the issue happens on another supported network only if safe and practical.
- Check service status and recent crash/error telemetry through approved tools.
- Record exact reproduction steps and whether the player can reach the login screen.

**Escalation**

Group matching reports by build, OS and error signature. Send the client/release team the version, affected platforms, approximate start time, error code, reproduction rate and examples with personal data redacted. Don't recommend reinstalling or clearing data until account/data sync implications are understood.

## GS-004 — High ping and disconnects

**Player message**

> My ping jumps from 40 to 250 and I get kicked from matches. Other apps seem fine.

**Simulated priority:** P2 for repeated match disruption; P3 for intermittent single-session symptoms without broader impact.

**First response (EN)**

> That sounds disruptive, especially during a match. I'll help isolate the connection path. Please share your region, platform, approximate match times with timezone, displayed ping, and whether the disconnect happens in every match or only on a specific server/party.

**Triage**

1. Check current regional service and matchmaking status.
2. Record server/region, platform, match IDs if available, timestamps, ping range and disconnect code.
3. Distinguish latency spikes from packet loss, client performance and server-side incidents.
4. Compare other reports with the same region/server and time window.
5. If approved, offer a low-risk test such as switching between wired and Wi-Fi; avoid asking for broad network scans or private router credentials.

**Escalation**

Send Network / Live Operations the region, time window, match references, observed latency and scope. Keep the ticket linked to any incident. Do not claim the player's ISP or the game server is at fault until evidence supports it.

## GS-005 — Ban appeal

**Player message**

> I was banned for cheating, but I didn't use anything. Remove the ban now.

**Simulated priority:** P2; apply the published appeal timeline and policy.

**First response (EN)**

> I understand that this is important to you. I can help submit an appeal for review. Please provide the account reference and any relevant context through the official appeal form. I can't promise a particular outcome, but the moderation team will review the case under the applicable policy.

**Triage**

- Verify the account through the approved workflow.
- Record the enforcement reference, date/time, game mode and the player's explanation.
- Check whether an appeal already exists and avoid duplicate submissions.
- Do not disclose detection signals, anti-cheat internals or other players' information.
- Do not overturn or shorten enforcement without explicit authority.

**Escalation**

Route to the moderation / enforcement review queue. Include the appeal reference, player's stated context and relevant timestamps. Communicate the expected review process without guaranteeing a deadline not published by the company.

## GS-006 — Toxicity / abusive behavior report

**Player message**

> This player keeps sending abusive messages and says they will find me outside the game. I've got screenshots.

**Simulated priority:** P2; P1 if there is a credible, immediate threat or an imminent real-world safety risk.

**First response (EN)**

> I'm sorry you're dealing with this. Thank you for reporting it. Please use the in-game report option if available and keep the original evidence. Don't engage with the player or share personal information. I'll route the report to the moderation team; if you believe there is an immediate real-world danger, contact local emergency services.

**Triage**

1. Collect player/report references, match or chat ID, timestamps and relevant screenshots through approved channels.
2. Preserve original evidence; don't edit or redistribute it unnecessarily.
3. Identify threats, doxxing, targeted harassment, repeated contact or other urgent safety indicators.
4. Use the approved moderation escalation path and restrict access to sensitive evidence.
5. Do not promise a specific punishment or reveal enforcement actions taken against another account.

**Escalation**

Immediate moderation/safety review for credible threats or doxxing. Include objective evidence, exact wording where necessary, timestamps, affected accounts and the urgency rationale. Avoid speculative conclusions about identity or intent.
