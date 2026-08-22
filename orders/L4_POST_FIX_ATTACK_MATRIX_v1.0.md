# UAi Post-Fix L4 Attack Matrix v1.0 (bus mirror)

**ID:** UAI-L4-POSTFIX-001  
**Status:** FROZEN  
**Target was:** 0.02-r100c30-fix4  
**D1 fix package:** 0.02-r100c30-fix4-d1  

Full matrix lives on Grok surface: project `artifacts/UAi/L4_POST_FIX_ATTACK_MATRIX_v1.0.md`.

## Battery D (controlling residual)

| ID | Attack | Expected after D1 fix |
|----|--------|------------------------|
| D1 | Gen-1 signed anchor after gen-2 floor; corrupt identity | authority=UNKNOWN; RECOVERY_REQUIRED; no promote/cwrite |
| D2 | Anchor only | Document + provenance |
| D3 | Truncated anchor | Fail closed |
| D4 | Wrong HMAC | Reject |

## Active order
`orders/ORD-UAI-D1-RETEST-L4-001.md`
