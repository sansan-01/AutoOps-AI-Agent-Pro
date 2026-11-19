import subprocess


_COMMANDS = {
    ("df", "-h"): ("/usr/bin/df", "-h"),
    ("free", "-h"): ("/usr/bin/free", "-h"),
    ("uptime",): ("/usr/bin/uptime",),
}


def execute_command(cmd: str) -> str:
    argv = _COMMANDS.get(tuple(cmd.split()))
    if argv is None:
        raise ValueError("Command is outside the diagnostic allowlist")

    try:
        result = subprocess.run(
            argv,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=True,
        )
    except subprocess.TimeoutExpired:
        return "诊断命令超时"
    except subprocess.CalledProcessError:
        return "诊断命令执行失败"
    return result.stdout
