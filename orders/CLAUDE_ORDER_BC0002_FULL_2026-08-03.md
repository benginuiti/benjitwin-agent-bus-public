# CLAUDE ORDER — Benjitwin BC-0002 Full Update
**Order ID:** CLAUDE-ORD-BC0002-FULL-2026-08-03
**From:** Browser Grok
**To:** Local Claude on BenX570E
**Priority:** P0
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
| Intake (drop zone) | `E:\\Benjitwin_Intake` |
| Processed originals | `E:\\Benjitwin_Processed` |

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
New-Item -ItemType Directory -Path "E:\\Benjitwin_Intake" -Force | Out-Null
New-Item -ItemType Directory -Path "E:\\Benjitwin_Processed" -Force | Out-Null
Write-Host "Architecture + Intake + Processed ready."
Get-ChildItem "E:\\Wizbangers" | Select-Object Name
```

---

## STEP 2 — Install governance documents

Create folder:

```
E:\\o2a-dev\\benjitwin_media\\BC0002\\
```

(or twin shared workspace if different — record actual path)

Write the files listed below. Full content is in the EMBEDDED DOCUMENTS section of this same order file (DOC-A through DOC-H). If this order file is truncated in transit, fetch the complete version from:

https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/orders/CLAUDE_ORDER_BC0002_FULL_2026-08-03.md

Required filenames:
- BC-0002_Recursive_Knowledge_Recovery_Living_WIZBANGERS.md (DOC-A)
- BC-0002_STATUS.md (DOC-B)
- FILESYSTEM_ROOTS_CONFIRMED.md (DOC-C)
- WIZBANGERS_STRUCTURE_v0.1.md (DOC-D)
- SEED_SET_v0.1.yaml (DOC-E)
- CANDIDATE_SET_v0.1.yaml (DOC-F)
- ARTIFACT_REGISTRY_SCHEMA.md (DOC-G)
- PROCESSING_SEQUENCE.md (DOC-H)

Also place a short pointer under `E:\\Wizbangers\\00_CONSTITUTION\\Registry\\`:

```
BC-0002 governance installed at: <actual path>
Installed: 2026-08-03
Status: Draft for Ben Approval (structure + roots locked)
```

---

## STEP 3 — Operating rules (enforce now)

1. Select artifacts **only** from `E:\\Benjitwin_Intake`
2. Max concurrent artifacts = **1**
3. Full Understanding Report required; stop and wait for Ben
4. Managed copy under `E:\\Wizbangers\\...` first, verify hash, then move original to `E:\\Benjitwin_Processed` (flat)
5. No deletes, no overwrites, no silent merges
6. Discovery folder is provisional only
7. Do not treat BC-0002 as fully Approved until Ben says so

---

## STEP 4 — Report (write to reports/LATEST.md)

```yaml
order_id: CLAUDE-ORD-BC0002-FULL-2026-08-03
timestamp: <ISO>
status: COMPLETE | PARTIAL | BLOCKED
folders_created:
  - E:\\Wizbangers (list top-level children)
  - E:\\Benjitwin_Intake
  - E:\\Benjitwin_Processed
governance_install_path: <full path>
governance_files:
  - <list>
intake_path_confirmed: E:\\Benjitwin_Intake
processed_path_confirmed: E:\\Benjitwin_Processed
max_concurrent_artifacts: 1
blockers: []
next_recommended_action: "Await Ben approval of BC-0002 + first drop into Intake"
```

---

## DO NOT

- Scan whole E: drive
- Move any files from outside Intake
- Promote identifiers/classifiers
- Raise concurrent authority
- Invent live O2A/YEP numbers

---

## NOTE ON EMBEDDED DOCS

The full embedded DOC-A through DOC-H content (BC-0002 contract, status, roots, structure, seed identifiers, classifiers, registry schema, processing sequence) lives in the portfolio copy and in the complete order file.

**Local portfolio path (Grok artifacts):**
`GROK_PUSHFORWARD_EVERYTHING/03_PORTFOLIO/BENJITWIN/CLAUDE_ORDER_BC0002_FULL_2026-08-03.md`

**Also available as individual files under:**
- `03_PORTFOLIO/BENJITWIN/00_CONSTITUTION/`
- `03_PORTFOLIO/LIVING_REGISTRY/`
- `03_PORTFOLIO/BENJITWIN/REGISTRY/`

If Claude can reach the Grok project artifacts or the full raw order, use those. Otherwise create the folders (Step 1) and write the pointer + a stub that lists the required governance filenames so Ben can copy the docs in one shot.

**Minimum success:** folders exist + report written. Governance file install is best-effort if content transfer is limited.

End of order.
