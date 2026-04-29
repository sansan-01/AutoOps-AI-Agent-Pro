# AutoOps AI Agent Pro

一个可运行的多Agent运维系统（带LLM、日志分析、推理、自动命令生成与执行、历史记忆与简单Web面板）。

## 运行
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=你的key  # 可选，无则使用内置兜底策略
python app.py
```
打开：http://localhost:5000

## 路由
- `/run`：执行一次完整链路（监控→日志→推理→行动）
- `/history`：最近10条历史案例

## 说明
- 默认关闭自动执行（AUTO_EXECUTE=False）
- 日志文件：logs/system.log
