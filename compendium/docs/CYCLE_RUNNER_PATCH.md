# cycle_runner.py integration (applied on X550 2026-11-14; original saved as backups/cycle_runner.pre_dkd_v2.py)

Inserted after the hunt part, inside the existing CYCLE.lock and before BEEP:

```python
   try:
    from bind_sources import cycle as bind_cycle
    bv=bind_cycle(max_requests=30)
    result["parts"]["binder"]=bv["outcome"]
    result["new_bindings"]=bv.get("new",0)
    if bv.get("new"):
     from ingest_dossier_v2 import run as dossier_run
     dr=dossier_run(refresh_only=True,locked=True)
     result["parts"]["dossier_refresh"]="PASS"
     result["dossier_bound"]=dr.get("bound")
   except Exception as e:
    result["parts"]["binder"]="BLOCKED:"+type(e).__name__
```
The binder never blocks the cycle, and cycle PASS still depends only on wave and recursive. At about 1.1 s per request, the binder adds roughly 35 s to each 5-minute cycle.
