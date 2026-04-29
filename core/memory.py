import json, os, time

DB = "memory.json"

def save_case(case: dict):
    data = []
    if os.path.exists(DB):
        try:
            with open(DB, "r") as f:
                data = json.load(f)
        except:
            data = []
    case["ts"] = int(time.time())
    data.append(case)
    with open(DB, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def list_cases(limit=10):
    if not os.path.exists(DB):
        return []
    with open(DB, "r") as f:
        data = json.load(f)
    return data[-limit:]
