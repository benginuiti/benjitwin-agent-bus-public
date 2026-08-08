# ORDER — UAi Mac surface → X570 host
**Order ID:** ORD-UAI-MAC-SURFACE-001
**Priority:** P0
**From:** Browser Grok
**To:** Local Claude on Mac (reneas-macbook-pro)
**Authority:** Ben
**Mode:** EXECUTE — no redesign
**Sign:** Browser Grok

---

## Goal (one sentence)

UAi iPhone app on BensPhone sends Think to the X570 UAi host and receives a real expedition id (no ATS block).

---

## Non-negotiables

1. Ben alone promotes and accepts.
2. Do not redesign UAi architecture or cognitive primitives.
3. Phone is a **surface only**; canonical UAi runs on X570 host.
4. Host URL is fixed: `http://100.95.127.31:49500`
5. **No secrets on this bus.** Bearer token already exists on host / local machine only — do not commit tokens, Keychain values, or passwords to git or this repo.
6. Do not change Cloudflare, DNS, or unrelated Wizbangers systems.
7. Do not collide with port 49400 (Benjitwin relay).
8. Receipt required. Stop only for one real blocker.

---

## Context (already true — do not rebuild)

| Item | Status |
|------|--------|
| UAi host on benx570e | Live at `http://100.95.127.31:49500` |
| Host tests | 14/14 PASS |
| Auth | Bearer required (401 without / 200 with) |
| Think on host | Produces expedition ids, persisted on X570 |
| Xcode UAi project | Exists on Mac (Team Benjamin Baird, device BensPhone) |
| Tailscale | benx570e `100.95.127.31`, iphone182 `100.95.61.86`, reneas-macbook-pro `100.127.243.61` |

---

## Exact work

1. Locate `UAi.xcodeproj` on this Mac; record absolute path in the receipt.
2. Ensure the app Think path calls:
   - `POST http://100.95.127.31:49500/uai/v0/think`
   - Header `Authorization: Bearer <token>` where token is read from local secure storage or existing local config — **not** from this order file.
3. Fix **App Transport Security** so cleartext HTTP to the Tailscale host is allowed for this personal app (`NSAllowsLocalNetworking` and/or `NSAllowsArbitraryLoads` as required to clear error -1022).
4. Build and run on **BensPhone** (development signing, team Benjamin Baird).
5. Execute or guide one **Think** on the phone with a unique phrase containing `ORD-UAI-MAC-SURFACE-001`.
6. Confirm host accepted Think (banner/response shows host OK / expedition id; optional Mac-side curl to host expeditions if token available locally).
7. Write receipt (path below).

---

## Do not

- Put bearer token in source committed to git or in bus files
- Redesign tabs / Gap Forge / Chrono
- Point surface at any host other than `100.95.127.31:49500`
- App Store / TestFlight requirement for this bite
- Modify X570 host API unless required to unblock surface proof (prefer surface-only fixes)

---

## Hard limits

- Max concurrent = 1 (this order only)
- No placement of Intake artifacts
- No production deploy

---

## Success criteria

- [ ] Build succeeds for BensPhone
- [ ] Think does **not** fail with ATS / NSURLError -1022
- [ ] Response or banner indicates host Think OK and an expedition id
- [ ] Prefer independent evidence: new expedition visible on X570 host store/API
- [ ] Receipt written with paths, commands, PASS/FAIL

---

## Receipt format

Write: `reports/RECEIPT_ORD-UAI-MAC-SURFACE-001.md` (this repo) **or** local Mac path recorded in that report if push not available.

Must include:

```yaml
order_id: ORD-UAI-MAC-SURFACE-001
timestamp_utc: 
project_path: 
device: BensPhone
ats_fix: 
think_result: PASS|FAIL
expedition_id: 
blocker: null|string
result: PASS|BLOCKED
```

---

## Return line

`ORD-UAI-MAC-SURFACE-001 — PASS`  
or  
`ORD-UAI-MAC-SURFACE-001 — BLOCKED: <single blocker>`
