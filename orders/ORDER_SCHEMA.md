# Order Schema (Strict)

**Authority:** Bus protocol  
**Applies to:** Executable order files under `orders/` matching:
- `CLAUDE_*.md`
- `ORD_*.md`
- Any file explicitly referenced by `orders/NEXT.md` as the active order

`NEXT.md` itself has a lighter schema (see below).  
`BC-*.md` governance documents are **not** required to follow the executable-order schema.

---

## Required fields (executable orders)

Every executable order **must** contain the following (case-insensitive, markdown bold optional):

| Field | Example | Rule |
|-------|---------|------|
| Order ID | `**Order ID:** CLAUDE-ORD-FIRST-UNDERSTANDING-2026-08-03` | Must match `^[A-Z0-9][A-Z0-9_-]+$` after the label |
| Priority | `**Priority:** P0` | One of: `P0`, `P1`, `P2`, `P3` |
| From | `**From:** Browser Grok` | Non-empty |
| To | `**To:** Local Claude on BenX570E` | Non-empty |
| Sign | `**Sign:** Browser Grok` | Near end of file |

### Strongly recommended (warned if missing)

- Hard limits / constraints section
- Success criteria or Success section
- Receipt format (YAML block preferred)
- Explicit STOP / wait-for-Ben language when the order produces an Understanding Report

---

## NEXT.md schema (lighter)

`orders/NEXT.md` must contain:

- `Updated:` (timestamp)
- `Priority:`
- `From:`
- Reference to an active order (Order ID or filename under `orders/`)
- `Sign:`

---

## Validation behavior

| Severity | Condition |
|----------|-----------|
| **FAIL** (blocks merge / push validation) | Missing Order ID, Priority, From, To, or Sign on an executable order |
| **FAIL** | Order ID does not match allowed pattern |
| **FAIL** | Priority not in {P0,P1,P2,P3} |
| **WARN** | Missing Hard limits / Success / Receipt format |
| **FAIL** | `NEXT.md` missing Updated / Priority / From / Sign or active-order reference |

GitHub Actions workflow `validate-bus.yml` enforces this on every push and PR to `main`.
