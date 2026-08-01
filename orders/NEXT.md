# ORDER — 2026-08-01D  P0 CHATBOT MVP

**From:** Browser Grok (BEN-authorized)
**To:** Local Claude (BenX570E)
**Priority:** BEN wants Benjitwin usable as a chatbot NOW — not multi-AI orchestration.

Defer evidence-supply / UI-02 art. Poller install only if not already done.

## Goal
One URL on the phone (Tailscale mesh) where BEN types a message, gets a durable reply path, without opening Claude/GPT/Grok.

## Build (read-first, then implement)

### A) Chat page on the relay (mesh-only bind as today)
Serve a simple mobile HTML page at GET /chat (or / ) that is a basic chatbot UI:
- Text input + Send
- Message list (local session + load recent from receipts if easy)
- Bearer token: prompt once, store in sessionStorage (not local disk secrets file)
- Calls existing POST /intention (or extend if needed) with content = user message
- Shows receipt_id + hub_forward result honestly (ok / fail / work_id)

No OpenMCT required on this page. Plain HTML/JS served by FastAPI (static or inline TemplateResponse).

### B) Reply path (minimum viable)
Today /intention creates hub work + receipt. Chatbot needs a visible answer.

Minimum acceptable for this bite:
1. User message -> receipt + hub work (already mostly done)
2. Auto-append a structured twin acknowledgment into the chat UI from the receipt response (receipt_id, work_id, status) — honest, not fake intelligence
3. Document next bite for real twin reasoning (hub worker or O2A) — do not invent model replies

If hub already has a read route for work by id, show that status in the chat thread after send.

### C) Phone URL
Document exact URL: http://100.95.127.31:49400/chat (or whatever path you use)
Keep /mct/ working. Keep token gate on /intention. /chat page itself may be mesh-gated like /mct (no bearer on static HTML) but API calls send bearer.

### D) Proofs (Claude measures, not BEN)
- GET /chat 200 on mesh IP
- POST /intention still 200 with receipt
- /health 200
- Backup relay_app.py before edit
- REPORT_LATEST.md with URL + what works / what is still acknowledgment-only

## Do not
- Fabricate AI answers as if twin reasoned
- Expose 8020 to mesh
- Ask BEN to configure GitHub or test as QA labor
- Unreal / full MCT redesign this bite

## Done when
BEN can open one URL on phone, type a sentence, see it accepted with receipt/work id in a chat-like UI — without talking to Claude/Grok/GPT for that message.

**Sign:** Browser Grok
