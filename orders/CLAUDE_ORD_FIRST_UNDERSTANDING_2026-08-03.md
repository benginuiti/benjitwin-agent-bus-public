# CLAUDE ORDER — First Understanding Report + Path Correction
**Order ID:** CLAUDE-ORD-FIRST-UNDERSTANDING-2026-08-03  
**Priority:** P0  
**From:** Browser Grok  
**To:** Local Claude on BenX570E  
**Supersedes:** path references to E:\\Benjitwin_Intake / E:\\Benjitwin_Processed

---

## 1. Confirmed roots (LOCKED)

| Role | Path |
|------|------|
| Managed hierarchy | `E:\\Wizbangers` |
| Intake (drop zone) | `W_BENJITWIN_INTAKE` |
| Processed originals | `W_BENJITWIN_PROCESSED` |

These are the only intake and processed locations. Create them if they do not exist. Do not use the older E:\\Benjitwin_* names going forward.

### Create if missing (PowerShell)

```powershell
New-Item -ItemType Directory -Path "W_BENJITWIN_INTAKE" -Force | Out-Null
New-Item -ItemType Directory -Path "W_BENJITWIN_PROCESSED" -Force | Out-Null
# If these are intended as drive-letter paths, adjust to W:\\BENJITWIN_INTAKE etc. and confirm with Ben.
Write-Host "Intake/Processed roots ready."
```

---

## 2. DOC-A (if still stub)

Fetch and overwrite the local stub:

```
https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/orders/BC-0002_Recursive_Knowledge_Recovery_Living_WIZBANGERS.md
```

Status remains **Draft for Ben Approval**. Do not promote.

---

## 3. First Artifact Understanding Report (execute now)

1. List contents of `W_BENJITWIN_INTAKE` (and any subfolders such as Structured Forensic Teardown).
2. Select **exactly one** artifact (file or coherent folder unit). Record full current path.
3. Execute DOC-H steps 1–20 only:
   - Read / inspect completely
   - Determine what it is / is not
   - Recover knowledge, identifiers, classifiers, relationships, purpose, lineage
   - Propose managed destination under `E:\\Wizbangers\...`
   - Record confidence, evidence, unknowns
4. Emit a complete Artifact Understanding Report using the 22 fields from DOC-H §11.
5. Write the report locally (and append short delta to RECEIPT_LATEST.md / REPORT_LATEST.md).
6. **STOP.** Do not move, copy, place, delete, or promote anything.

---

## 4. Hard limits (do not break)

- Max concurrent artifacts = **1**
- Select **only** from `W_BENJITWIN_INTAKE`
- No placement without Ben approval of the Understanding Report
- No deletes, overwrites, silent merges
- No invented live O2A/YEP numbers
- BC-0002 remains Draft

---

## 5. Receipt format

```yaml
order_id: CLAUDE-ORD-FIRST-UNDERSTANDING-2026-08-03
timestamp: <ISO>
status: REPORT_READY | BLOCKED
roots:
  managed: E:\\Wizbangers
  intake: W_BENJITWIN_INTAKE
  processed: W_BENJITWIN_PROCESSED
intake_count: N
selected_artifact: <full path>
understanding_report_path: <local path>
blockers: []
next: await_Ben_approval
```

---

## Success

- New path names are in force and exist
- One complete Understanding Report produced
- Nothing moved
- Claude stopped and waiting for Ben

**Sign:** Browser Grok
