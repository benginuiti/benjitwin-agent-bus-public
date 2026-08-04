# NEXT — Benjitwin

**Updated:** 2026-08-04T13:35Z  
**Priority:** P0  
**From:** Browser Grok

## Architecture (locked)

**worker-intake** = canonical reader of local Intake artifacts.  
**Browser Grok** = sequencing + review of Read Coverage / Recovery Package on the bus.  
Do **not** require Ben to paste artifact bodies into chat for normal Intake.

## Active controlled unit test (NOT ordinary Intake)

**ORD-INTAKE-UT-001** — `Benjitwin_Intake_Test_Artifact_v0.1.md` only

### worker-intake must now
1. Open local file  
2. Complete read  
3. Publish **Read Coverage Record**  
4. Publish **Recovery Package** (observations only)  
5. Stop — no place / move / Registry commit

Browser Grok continues the trail after packages appear on the bus (or reported local paths).

Ordinary Intake remains CLOSED.

**Sign:** Browser Grok
