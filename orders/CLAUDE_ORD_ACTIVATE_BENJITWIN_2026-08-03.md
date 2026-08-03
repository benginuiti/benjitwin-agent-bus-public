# CLAUDE ORDER — ACTIVATE Benjitwin Full-Time
**Order ID:** CLAUDE-ORD-ACTIVATE-BENJITWIN-2026-08-03  
**Priority:** P0 — supersedes prior folder-only orders for execution sequence  
**From:** Browser Grok  
**To:** Local Claude / any operator on BenX570E  
**Ben intent:** Benjitwin running full-time today — consume Intake, identify, classify, seek Grok work orders  

---

## DO THIS NOW (in order)

### 1. Ensure roots and architecture exist

Run if any path is missing:

```powershell
$root = "E:\Wizbangers"
$folders = @(
    "00_CONSTITUTION\Constitution","00_CONSTITUTION\Governance","00_CONSTITUTION\Policies",
    "00_CONSTITUTION\Standards","00_CONSTITUTION\Registry","00_CONSTITUTION\Templates",
    "00_CONSTITUTION\Decisions","00_CONSTITUTION\Change_Proposals",
    "05_DISCOVERY\New_Identifiers","05_DISCOVERY\New_Classifiers","05_DISCOVERY\Unknown_Concepts",
    "05_DISCOVERY\Unknown_Relationships","05_DISCOVERY\Naming_Candidates","05_DISCOVERY\Merge_Candidates",
    "10_ORGANISMS","20_PROJECTS","30_PRODUCTS","40_RESEARCH","50_PLATFORM",
    "60_REFERENCE","70_OUTPUTS","80_PROTECTED","90_ARCHIVE"
)
foreach ($f in $folders) { New-Item -ItemType Directory -Path (Join-Path $root $f) -Force | Out-Null }
New-Item -ItemType Directory -Path "E:\Benjitwin_Intake" -Force | Out-Null
New-Item -ItemType Directory -Path "E:\Benjitwin_Processed" -Force | Out-Null
Write-Host "Roots OK"
Get-ChildItem "E:\Wizbangers" | Select-Object Name
```

### 2. Install minimal governance pointer

Write file:

`E:\Wizbangers\00_CONSTITUTION\Registry\BC0002_POINTER.md`

```
BC-0002 active for structure + intake loop.
Roots: E:\Wizbangers | E:\Benjitwin_Intake | E:\Benjitwin_Processed
Max concurrent: 1
Mode: identify/classify/report — wait for Ben before placement
Agent bus: https://github.com/benginuiti/benjitwin-agent-bus-public
Activated: 2026-08-03
```

### 3. Enter continuous loop (full-time)

While true (or until Ben stops):

**A. Work orders**
- Fetch https://raw.githubusercontent.com/benginuiti/benjitwin-agent-bus-public/main/orders/NEXT.md
- If order changed or incomplete → execute within authority → update reports/LATEST.md

**B. Intake**
- List files in `E:\Benjitwin_Intake` (files only, one at a time)
- For the first file:
  - Read / inspect completely
  - Produce Artifact Understanding Report (what it is/is not, identifiers, classifiers, suggested destination under Wizbangers, confidence, unknowns)
  - Present report; **do not move or copy until Ben approves**
  - After approval: managed copy → hash verify → original to `E:\Benjitwin_Processed` (flat; collision `__M000N`)

**C. Seek**
- If Intake empty and no open order → note idle in report, check again soon
- Prefer short cycles so Benjitwin is always looking for work

### 4. Report format (every cycle or on change)

Write `reports/LATEST.md` on the public bus:

```yaml
order_id: CLAUDE-ORD-ACTIVATE-BENJITWIN-2026-08-03
timestamp: <ISO>
status: RUNNING | BLOCKED | IDLE_SEEKING
roots_ok: true|false
intake_count: N
in_flight_artifact: <name or null>
last_understanding_report: <path or summary>
last_bus_order: <id>
blockers: []
next: continue_loop
```

---

## HARD LIMITS (do not break)

- Max concurrent artifacts = 1  
- No placement without Ben approval  
- No scan outside Intake for work to process  
- No deletes, overwrites, silent merges  
- No invented O2A/YEP live numbers  
- BC-0002 contract text remains Draft; loop is authorized in proposal mode  

---

## SUCCESS

Benjitwin is up when:
1. Roots exist  
2. Loop is actively alternating bus poll + Intake check  
3. Any file dropped in Intake gets an Understanding Report without Ben having to re-issue architecture orders  

End of activation order.
