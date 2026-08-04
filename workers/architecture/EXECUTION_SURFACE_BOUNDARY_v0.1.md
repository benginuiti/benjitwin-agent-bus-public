# Execution-surface boundary v0.1
**Status:** BEN_DECLARED 2026-08-04  
**Authority:** Architectural correction (controlled unit test preserved)

## Division

### worker-intake (local)
- opens local artifact
- reads artifact completely
- proves Read Coverage
- produces Recovery Package
- publishes Read Coverage and Recovery Package to the bus

### Browser Grok
- reviews Read Coverage
- audits Recovery Package
- verifies Understanding
- verifies Classification
- verifies Integrity
- controls sequencing

Browser Grok is **not** the reader.  
worker-intake **is** the reader.

## Law

Do not require manual artifact pasting into chat for normal Intake operation when a local Benjitwin worker owns the artifact.

Controlled unit tests use the same boundary.
