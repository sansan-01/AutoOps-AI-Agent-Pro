def reason(status, log_analysis, llm):
    prompt = f"""
系统状态:
{status}

日志分析:
{log_analysis}

请进行分步骤推理（chain-of-thought），给出最可能的根因排序（Top3），并给出验证方法。
"""
    return llm(prompt)
