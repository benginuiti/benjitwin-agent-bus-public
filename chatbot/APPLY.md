# Apply Benjitwin Chat MVP on BenX570E

## Files
- `chatbot/chat.html` — mobile chat UI (this repo)

## Steps
1. Backup `E:\o2a-dev\benjitwin_relay\relay_app.py`
2. Download chat.html to `E:\o2a-dev\benjitwin_relay\static\chat.html` (create static dir)
3. In relay_app.py:
   - Ensure StaticFiles or a FileResponse route for chat
   - Preferred routes:
     - `GET /chat` -> chat.html
     - `GET /` -> redirect to /chat (optional)
   - Do NOT put require_relay_auth on GET /chat (browser has no header on first paint). Token stays on POST /intention only.
4. Restart relay the same way it is currently started (mesh bind 100.95.127.31:49400, token process env only)
5. Prove:
   - `curl -s -o NUL -w %{http_code} http://100.95.127.31:49400/chat` -> 200
   - `curl -s http://100.95.127.31:49400/health` -> 200
   - POST /intention still requires bearer
6. Write REPORT_LATEST.md with phone URL: `http://100.95.127.31:49400/chat`

## Minimal FastAPI pattern (adapt to existing app object name)

```python
from pathlib import Path
from fastapi.responses import FileResponse, RedirectResponse

STATIC = Path(__file__).resolve().parent / "static"

@app.get("/chat")
async def chat_page():
    return FileResponse(STATIC / "chat.html", media_type="text/html")

@app.get("/")
async def root_redirect():
    return RedirectResponse(url="/chat", status_code=307)
```

If StaticFiles already mounted, still add explicit /chat FileResponse for clarity.

## Done / REVIEW_READY
Phone can open /chat, enter token once per session, send a message, see receipt/work acknowledgment.
