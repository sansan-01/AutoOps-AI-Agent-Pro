import fcntl
import json
import os
import time
from pathlib import Path
from tempfile import NamedTemporaryFile

DB = "memory.json"

def _load_cases():
    try:
        with open(DB, "r", encoding="utf-8") as history:
            cases = json.load(history)
    except FileNotFoundError:
        return []
    if not isinstance(cases, list):
        raise ValueError("Analysis history must contain a JSON array")
    return cases


def save_case(case: dict):
    path = Path(DB)
    with open(f"{path}.lock", "a", encoding="utf-8") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        cases = _load_cases()
        timestamp = int(time.time())
        cases.append({**case, "ts": timestamp})

        tmp_path = None
        try:
            with NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=path.parent,
                prefix=f".{path.name}.", suffix=".tmp", delete=False,
            ) as tmp:
                tmp_path = Path(tmp.name)
                json.dump(cases, tmp, indent=2, ensure_ascii=False)
                tmp.flush()
                os.fsync(tmp.fileno())
            os.replace(tmp_path, path)
        finally:
            if tmp_path is not None:
                tmp_path.unlink(missing_ok=True)
        case["ts"] = timestamp


def list_cases(limit=10):
    return _load_cases()[-limit:]
