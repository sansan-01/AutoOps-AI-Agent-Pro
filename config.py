import os

AUTH_PASSWORD = os.getenv("AUTOOPS_AUTH_PASSWORD", "")
LLM_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL = os.getenv("MODEL", "gpt-4o-mini")
SEND_LOGS_TO_LLM = os.getenv("SEND_LOGS_TO_LLM") == "1"

# 安全：默认关闭自动执行
AUTO_EXECUTE = False

# 日志路径
LOG_PATH = os.getenv("LOG_PATH", "logs/system.log")
