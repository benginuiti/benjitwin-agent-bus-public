#!/usr/bin/env python3
"""Greenly verb host — 127.0.0.1 only. Learning lane. No WAN bind."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

BIND = "127.0.0.1"
PORT = 49410
UE_RC = "http://127.0.0.1:30010"


def probe_ue() -> dict:
    last = "no_attempt"
    for path in ("/remote/info", "/remote", "/"):
        try:
            req = urllib.request.Request(UE_RC + path, method="GET")
            with urllib.request.urlopen(req, timeout=2) as r:
                body = r.read().decode("utf-8", "replace")[:400]
                return {"up": True, "status": r.status, "path": path, "body": body}
        except Exception as exc:
            last = str(exc)
    return {"up": False, "error": last}


def try_hello_ue() -> dict:
    py = (
        "import unreal\n"
        "loc = unreal.Vector(0.0, 0.0, 120.0)\n"
        "actor = unreal.EditorLevelLibrary.spawn_actor_from_class("
        "unreal.StaticMeshActor, loc)\n"
        "actor.set_actor_label('GREENLY_HELLO')\n"
        "print('GREENLY_HELLO')\n"
    )
    payloads = [
        ("POST", "/remote/python/execute", {"command": py}),
        (
            "PUT",
            "/remote/object/call",
            {
                "objectPath": "/Script/PythonScriptPlugin.Default__PythonScriptLibrary",
                "functionName": "ExecutePythonCommand",
                "parameters": {"PythonCommand": py},
            },
        ),
    ]
    last = {"ok": False, "error": "no_attempt"}
    for method, path, body in payloads:
        try:
            data = json.dumps(body).encode("utf-8")
            req = urllib.request.Request(
                UE_RC + path,
                data=data,
                method=method,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=6) as r:
                return {
                    "ok": True,
                    "via": path,
                    "status": r.status,
                    "body": r.read().decode("utf-8", "replace")[:500],
                }
        except Exception as exc:
            last = {"ok": False, "via": path, "error": str(exc)}
    return last


class Handler(BaseHTTPRequestHandler):
    def _json(self, code: int, obj: dict) -> None:
        blob = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)

    def do_GET(self) -> None:
        if self.path in ("/", "/health", "/verb/status"):
            self._json(
                200,
                {
                    "ok": True,
                    "service": "greenly_verb_host",
                    "bind": f"{BIND}:{PORT}",
                    "ue": probe_ue(),
                },
            )
            return
        self._json(404, {"ok": False, "error": "not_found"})

    def do_POST(self) -> None:
        if self.path == "/verb/hello":
            ue = probe_ue()
            spawn = try_hello_ue() if ue.get("up") else {"ok": False, "error": "ue_remote_control_down"}
            self._json(
                200,
                {
                    "ok": True,
                    "hello": "GREENLY_HELLO",
                    "ue": ue,
                    "spawn": spawn,
                },
            )
            return
        if self.path == "/verb/status":
            self._json(200, {"ok": True, "ue": probe_ue()})
            return
        self._json(404, {"ok": False, "error": "not_found"})

    def log_message(self, *_args) -> None:
        return


if __name__ == "__main__":
    httpd = HTTPServer((BIND, PORT), Handler)
    print(f"greenly_verb_host {BIND}:{PORT}", flush=True)
    httpd.serve_forever()
