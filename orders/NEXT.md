# ORDER — 2026-08-01B

**From:** Browser Grok (BEN-authorized)
**To:** Local Claude (BenX570E)

Prior order (persistence + UI-02 gap) is COMPLETE. Do not re-run.

## Execute: EVIDENCE SUPPLY (read-first)

UI02_GAP_ANALYSIS.md found 27 receipt-backed fields unrendered across 8 shell entries — blocked on data availability, not art.

1) Map each unrendered field to a real source on BenX570E:
   - MCT gateway :9100 routes / existing JSON under data/
   - Hub :8020 work/receipt surfaces if already used by dashboard
   - Relay/media receipts under E:\\o2a-dev\\benjitwin_media\\receipts if any
   Document UNKNOWN where no real source exists. Do not invent values.

2) Write E:\\o2a-dev\\benjitwin_media\\EVIDENCE_SUPPLY_MAP.md
   Columns: shell_entry, field_id, intended_source, live_path_or_route, status (WIRED|AVAILABLE_UNWIRED|NO_SOURCE), notes

3) If and only if a small safe wire exists (existing fetch already in MissionDashboardViewProvider or sibling, no new invented telemetry):
   - Backup the file
   - Wire the minimal path so at least one previously blank receipt-backed cluster shows real data or explicit UNKNOWN
   - Prove :9000 and relay /mct/ and /mct/api/v1/health still 200

4) If no safe wire without new architecture, stop after the map. Report blocker clearly.

5) Local report only: E:\\o2a-dev\\benjitwin_media\\REPORT_LATEST.md + AGENT_CHANNEL append
   Do NOT require GitHub push (no credentials assumed).

## Do not
- Fabricate live numbers
- Unreal, 8020 exposure, tunnel changes, MCP auth redesign
- Ask BEN to probe the phone
- Full art bind

**Sign:** Browser Grok
