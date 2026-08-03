# CLAUDE ORDER — Benjitwin BC-0002 Update
**Order ID:** CLAUDE-ORD-BC0002-2026-08-03  
**From:** Grok (this surface)  
**To:** Local Claude / Benjitwin operator  
**Priority:** P0  
**Authority:** Ben confirmed filesystem roots; BC-0002 itself remains Draft for Ben Approval  

---

## 1. Objective

Update the local Benjitwin running instance with:

1. BC-0002 (Recursive Knowledge Recovery & Living WIZBANGERS Organization)
2. Confirmed filesystem roots (Ben 2026-08-03)
3. Initial folder architecture under the managed root
4. Single-artifact processing authority and intake loop

Do **not** invent live data. Do **not** move any real user files yet. Do **not** promote identifiers or classifiers. Create structure and governance only.

---

## 2. Confirmed filesystem roots (LOCKED by Ben)

| Role | Path | Action |
|------|------|--------|
| Managed hierarchy | `E:\Wizbangers` | Create full architecture (see §3) |
| Intake (drop zone) | `E:\Benjitwin_Intake` | Create if missing |
| Processed originals | `E:\Benjitwin_Processed` | Create if missing (flat — no subfolders) |

These names supersede any earlier placeholders (`E:\WIZBANGERS`, `E:\Processed`).

---

## 3. Create this exact architecture

```text
E:\Wizbangers\
├── 00_CONSTITUTION\
│   ├── Constitution\
│   ├── Governance\
│   ├── Policies\
│   ├── Standards\
│   ├── Registry\
│   ├── Templates\
│   ├── Decisions\
│   └── Change_Proposals\
├── 05_DISCOVERY\
│   ├── New_Identifiers\
│   ├── New_Classifiers\
│   ├── Unknown_Concepts\
│   ├── Unknown_Relationships\
│   ├── Naming_Candidates\
│   └── Merge_Candidates\
├── 10_ORGANISMS\
├── 20_PROJECTS\
├── 30_PRODUCTS\
├── 40_RESEARCH\
├── 50_PLATFORM\
├── 60_REFERENCE\
├── 70_OUTPUTS\
├── 80_PROTECTED\
└── 90_ARCHIVE\
```

Plus the two sibling roots:

```text
E:\Benjitwin_Intake\
E:\Benjitwin_Processed\
```

### PowerShell (run once)

```powershell
$root = "E:\Wizbangers"
$folders = @(
    "00_CONSTITUTION\Constitution",
    "00_CONSTITUTION\Governance",
    "00_CONSTITUTION\Policies",
    "00_CONSTITUTION\Standards",
    "00_CONSTITUTION\Registry",
    "00_CONSTITUTION\Templates",
    "00_CONSTITUTION\Decisions",
    "00_CONSTITUTION\Change_Proposals",
    "05_DISCOVERY\New_Identifiers",
    "05_DISCOVERY\New_Classifiers",
    "05_DISCOVERY\Unknown_Concepts",
    "05_DISCOVERY\Unknown_Relationships",
    "05_DISCOVERY\Naming_Candidates",
    "05_DISCOVERY\Merge_Candidates",
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
New-Item -ItemType Directory -Path "E:\Benjitwin_Intake" -Force | Out-Null
New-Item -ItemType Directory -Path "E:\Benjitwin_Processed" -Force | Out-Null
Write-Host "Architecture + Intake + Processed ready."
```

---

## 4. Install governance documents

Copy (or recreate) these files into the local Benjitwin surface / shared workspace so the twin can see them:

| Source (this portfolio) | Purpose |
|-------------------------|---------|
| `00_CONSTITUTION/BC-0002_Recursive_Knowledge_Recovery_Living_WIZBANGERS.md` | Full contract |
| `00_CONSTITUTION/BC-0002_STATUS.md` | Status + gate |
| `00_CONSTITUTION/FILESYSTEM_ROOTS_CONFIRMED.md` | Locked paths |
| `00_CONSTITUTION/WIZBANGERS_STRUCTURE_v0.1.md` | Structure reference |
| `LIVING_REGISTRY/identifiers/SEED_SET_v0.1.yaml` | Starting identifiers |
| `LIVING_REGISTRY/classifiers/CANDIDATE_SET_v0.1.yaml` | Starting classifiers |
| `REGISTRY/ARTIFACT_REGISTRY_SCHEMA.md` | Registry schema |
| `REGISTRY/PROCESSING_SEQUENCE.md` | 27-step sequence |

Preferred local target (if the twin uses a media / shared workspace folder):

```
E:\o2a-dev\benjitwin_media\  (or current shared workspace path)
  └── BC0002\
        ├── BC-0002_....md
        ├── FILESYSTEM_ROOTS_CONFIRMED.md
        └── ...
```

If the twin already has a Constitution / Governance location, place them there instead. Record the final path in the report.

---

## 5. Operating rules to enforce immediately

1. **Intake only** — Benjitwin may select artifacts exclusively from `E:\Benjitwin_Intake`.
2. **Max concurrent = 1** — process exactly one artifact at a time.
3. **Understanding before placement** — full Artifact Understanding Report required; stop and wait for Ben.
4. **Managed copy first** — write verified copy under `E:\Wizbangers\…` before touching the original.
5. **Originals land in** `E:\Benjitwin_Processed` (flat). Collision → neutral suffix `__M000N`. Never overwrite, never delete.
6. **Discovery is provisional** — nothing under `05_DISCOVERY` is authoritative until Ben promotes it.
7. **No structural changes** without a Change Proposal that Ben explicitly approves.

---

## 6. What Claude must NOT do

- Do not scan the whole E: drive.
- Do not move or copy any real user files from outside Intake.
- Do not promote any identifier or classifier beyond the seed set.
- Do not raise concurrent-artifact authority.
- Do not invent live O2A / YEP / registry numbers.
- Do not treat BC-0002 as fully approved until Ben says `Approved`.

---

## 7. Required report back

Write `reports/LATEST.md` (agent-bus) containing:

```yaml
order_id: CLAUDE-ORD-BC0002-2026-08-03
timestamp: <ISO>
status: COMPLETE | PARTIAL | BLOCKED
folders_created:
  - E:\Wizbangers\...
  - E:\Benjitwin_Intake
  - E:\Benjitwin_Processed
governance_files_installed:
  - <full paths>
intake_path_confirmed: E:\Benjitwin_Intake
processed_path_confirmed: E:\Benjitwin_Processed
max_concurrent_artifacts: 1
blockers: []
next_recommended_action: "Await Ben approval of BC-0002 + first drop into Intake"
```

---

## 8. Success criteria

- All three roots exist.
- Full Wizbangers architecture exists under `E:\Wizbangers`.
- Governance documents are visible to Benjitwin.
- Twin will only select from `E:\Benjitwin_Intake` and will stop after each Understanding Report.
- No real artifacts have been moved.

End of order.
