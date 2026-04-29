from config import LOG_PATH

def read_logs():
    try:
        with open(LOG_PATH, "r") as f:
            lines = f.readlines()
        return lines[-50:]
    except:
        return ["No logs found"]

def analyze_logs(llm):
    logs = read_logs()
    prompt = f"""
你是资深运维工程师，请对以下最近日志进行总结，指出异常类型、频率和可能影响：
{''.join(logs)}
"""
    return llm(prompt)
