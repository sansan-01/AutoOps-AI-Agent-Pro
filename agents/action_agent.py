from core.executor import execute_command
from config import AUTO_EXECUTE

def act(reasoning, llm):
    prompt = f"""
根据以下问题描述，生成最安全的Linux修复命令（避免破坏性操作）：
{reasoning}

只返回命令（单行）。
"""
    cmd = llm(prompt).strip().splitlines()[-1]

    if AUTO_EXECUTE and cmd:
        result = execute_command(cmd)
        return {"cmd": cmd, "executed": True, "result": result}
    return {"cmd": cmd, "executed": False, "result": "未执行（安全模式）"}
