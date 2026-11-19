from core.executor import execute_command
from config import AUTO_EXECUTE

def act(reasoning, llm):
    prompt = f"""
根据以下问题描述，生成最安全的Linux修复命令（避免破坏性操作）：
{reasoning}

只返回命令（单行）。
"""
    lines = llm(prompt).strip().splitlines()
    if not lines:
        return {"cmd": "", "executed": False, "result": "无可用命令"}

    cmd = lines[-1].strip()

    if AUTO_EXECUTE and cmd:
        try:
            result = execute_command(cmd)
        except ValueError:
            return {"cmd": cmd, "executed": False, "result": "命令不在诊断白名单中"}
        except OSError:
            return {"cmd": cmd, "executed": False, "result": "无法启动诊断命令"}
        return {"cmd": cmd, "executed": True, "result": result}
    return {"cmd": cmd, "executed": False, "result": "未执行（安全模式）"}
