import os

def execute_command(cmd: str) -> str:
    try:
        return os.popen(cmd).read()
    except Exception as e:
        return str(e)
