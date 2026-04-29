import os, requests, time
from config import LLM_API_KEY, MODEL

def _fallback(prompt: str) -> str:
    # 简单规则兜底，保证无API Key也能演示
    p = prompt.lower()
    if "502" in p:
        return "检测到大量502错误，可能是后端服务不可用或超时，优先检查后端服务与网关。"
    if "cpu" in p:
        return "CPU 使用率异常偏高，可能存在死循环/高负载任务，建议定位占用最高的进程。"
    return "未检测到明显异常，请进一步检查。"

def call_llm(prompt: str) -> str:
    if not LLM_API_KEY:
        return _fallback(prompt)

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    try:
        res = requests.post(url, headers=headers, json=data, timeout=30)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"LLM调用失败，使用兜底策略。错误：{e}\n{_fallback(prompt)}"
