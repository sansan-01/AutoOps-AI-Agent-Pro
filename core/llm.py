import logging
import re

import requests

from config import LLM_API_KEY, MODEL

logger = logging.getLogger(__name__)


def _fallback(prompt: str) -> str:
    # 简单规则兜底，保证无API Key也能演示
    if re.search(r"\b502\b", prompt):
        return "发现 502 相关文本。若为 HTTP 502，请检查后端服务与网关。"
    return "本地规则无法确认根因，请结合系统指标和日志进一步检查。"

def call_llm(prompt: str, *, allow_remote: bool = True, use_fallback: bool = True) -> str:
    if not allow_remote or not LLM_API_KEY:
        return _fallback(prompt) if use_fallback else ""

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
        res = requests.post(
            url, headers=headers, json=data, timeout=(5, 30), allow_redirects=False
        )
        res.raise_for_status()
        if res.status_code != 200:
            raise ValueError("Unexpected LLM response status")
        content = res.json()["choices"][0]["message"]["content"]
        if not isinstance(content, str) or not content.strip():
            raise ValueError("Missing LLM response content")
        return content
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        logger.warning("LLM request failed")
        return _fallback(prompt) if use_fallback else ""
