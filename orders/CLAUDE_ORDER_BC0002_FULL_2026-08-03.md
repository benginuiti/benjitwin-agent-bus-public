# CLAUDE ORDER — Benjitwin BC-0002 Full Update
**Order ID:** CLAUDE-ORD-BC0002-FULL-2026-08-03
**Priority:** P0
**From:** Browser Grok
**To:** Local Claude on BenX570E
**Mode:** Execute and report

---

## OBJECTIVE

1. Create the confirmed filesystem roots and full Wizbangers architecture.
2. Install BC-0002 governance documents into a local path Benjitwin can read.
3. Confirm intake-only + max concurrent = 1 rules are in force.
4. Report exact paths created. Do not move any real user artifacts.

---

## CONFIRMED ROOTS (Ben locked 2026-08-03)

| Role | Path |
|------|------|
| Managed hierarchy | `E:\\Wizbangers` |
| Intake (drop zone) | `W_BENJITWIN_INTAKE` |
| Processed originals | `W_BENJITWIN_PROCESSED` |

---

## STEP 1 — Create folders (run this PowerShell)

```powershell
$root = "E:\\Wizbangers"
$folders = @(
    "00_CONSTITUTION\\Constitution",
    "00_CONSTITUTION\\Governance",
    "00_CONSTITUTION\\Policies",
    "00_CONSTITUTION\\Standards",
    "00_CONSTITUTION\\Registry",
    "00_CONSTITUTION\\Templates",
    "00_CONSTITUTION\\Decisions",
    "00_CONSTITUTION\\Change_Proposals",
    "05_DISCOVERY\\New_Identifiers",
    "05_DISCOVERY\\New_Classifiers",
    "05_DISCOVERY\\Unknown_Concepts",
    "05_DISCOVERY\\Unknown_Relationships",
    "05_DISCOVERY\\Naming_Candidates",
    "05_DISCOVERY\\Merge_Candidates",
    "10_ORGANISMS",
    "20_PROJECTS",
    "30_PRODUCTS",
    "40_RESEARCH",
    "50_PLATFORM",
    "60_REFERENCE",
    "70_OUTPUTS",
    "80_PROTECTED",
    "90_ARCHIVE"
)
foreach ($f in $folders) {
    New-Item -ItemType Directory -Path (Join-Path $root $f) -Force | Out-Null
}
New-Item -ItemType Directory -Path "W_BENJITWIN_INTAKE" -Force | Out-Null
New-Item -ItemType Directory -Path "W_BENJITWIN_PROCESSED" -Force | Out-Null
Write-Host "Architecture + Intake + Processed ready."
Get-ChildItem "E:\\Wizbangers" | Select-Object Name
```

---

## STEP 2 — Install governance documents

Create folder:

```
E:\\o2a-dev\\benjitwin_media\\BC0002\\
```

Write the required governance filenames (DOC-A through DOC-H). Full text available on the bus and in the portfolio.

Also place a short pointer under `E:\\Wizbangers\\00_CONSTITUTION\\Registry\\`.

---

## STEP 3 — Operating rules (enforce now)

1. Select artifacts **only** from `W_BENJITWIN_INTAKE`
2. Max concurrent artifacts = **1**
3. Full Understanding Report required; stop and wait for Ben
4. Managed copy under `E:\\Wizbangers\\...` first, verify hash, then move original to `W_BENJITWIN_PROCESSED` (flat)
5. No deletes, no overwrites, no silent merges

---

## STEP 4 — Report (write to reports/LATEST.md)

```yaml
order_id: CLAUDE-ORD-BC0002-FULL-2026-08-03
timestamp: <ISO>
status: COMPLETE | PARTIAL | BLOCKED
folders_created: []
governance_install_path: <full path>
max_concurrent_artifacts: 1
blockers: []
next_recommended_action: "Await Ben approval of BC-0002 + first drop into Intake"
```

---

## DO NOT

- Scan whole drives
- Move any files from outside Intake
- Promote identifiers/classifiers
- Invent live O2A/YEP numbers

**Sign:** Browser Grok
