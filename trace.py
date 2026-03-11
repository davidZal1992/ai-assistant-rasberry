#!/usr/bin/env python3
"""Lightweight request tracing — logs step durations to ~/.smarthome_trace.jsonl"""
import json, time, os
from contextlib import contextmanager

TRACE_LOG = os.path.expanduser("~/.smarthome_trace.jsonl")

class Trace:
    def __init__(self, request_id: str):
        self.request_id = request_id
        self.start = time.monotonic()
        self.steps = []

    @contextmanager
    def step(self, name: str):
        t0 = time.monotonic()
        error = None
        try:
            yield
        except Exception as e:
            error = str(e)
            raise
        finally:
            elapsed = (time.monotonic() - t0) * 1000
            entry = {"step": name, "ms": round(elapsed, 1)}
            if error:
                entry["error"] = error
            self.steps.append(entry)
            marker = "ERR" if error else ("SLOW" if elapsed > 2000 else "OK")
            print("[TRACE] {} {}: {:.0f}ms".format(marker, name, elapsed), flush=True)

    def finish(self, status="ok"):
        total = (time.monotonic() - self.start) * 1000
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "id": self.request_id,
            "total_ms": round(total, 1),
            "status": status,
            "steps": self.steps,
        }
        with open(TRACE_LOG, "a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        if self.steps:
            bottleneck = max(self.steps, key=lambda s: s["ms"])
            print("[TRACE] BOTTLENECK: {} ({:.0f}ms) | total: {:.0f}ms".format(
                bottleneck["step"], bottleneck["ms"], total))
        return record
