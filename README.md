# AutoOps AI Agent Pro

一个可运行的多Agent运维系统（带LLM、日志分析、推理、自动命令生成与执行、历史记忆与简单Web面板）。

## 运行

需要 Linux 和 Python 3.10 或更高版本。

```bash
python3 -m pip install -r requirements.txt
read -rsp 'AutoOps password ' AUTOOPS_AUTH_PASSWORD
printf '\n'
export AUTOOPS_AUTH_PASSWORD
python3 app.py
```

打开 `http://127.0.0.1:5000`，使用用户名 `autoops` 和配置的强密码登录。应用默认仅监听本机。远程部署时，请通过 HTTPS 提供访问。

环境变量见 `.env.example`。可选配置 `OPENAI_API_KEY` 以启用远程推理和命令建议。原始日志默认在本机分析。仅在确认日志可发送到 OpenAI 后设置 `SEND_LOGS_TO_LLM=1`。

## 路由

- `POST /run` 执行一次完整链路（监控→日志→推理→行动）。API 调用需要 HTTP Basic 认证和 `X-AutoOps-Request: 1` 请求头。
- `GET /history` 使用同样的认证读取最近 10 条历史案例。

## 说明

- 默认关闭自动执行（`AUTO_EXECUTE=False`）。开启后，只允许自动运行预设的只读诊断命令。执行其他建议前请人工检查。
- 默认读取本地 `logs/system.log`。可通过 `LOG_PATH` 指定现有日志文件。
