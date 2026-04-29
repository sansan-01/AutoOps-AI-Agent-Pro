from flask import Flask, jsonify, render_template
from agents.monitor import get_system_status
from agents.log_agent import analyze_logs
from agents.reasoning_agent import reason
from agents.action_agent import act
from core.llm import call_llm
from core.memory import save_case, list_cases

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run")
def run():
    status = get_system_status()
    log_analysis = analyze_logs(call_llm)
    reasoning = reason(status, log_analysis, call_llm)
    action = act(reasoning, call_llm)

    case = {
        "status": status,
        "analysis": log_analysis,
        "reasoning": reasoning,
        "action": action
    }
    save_case(case)

    return jsonify(case)

@app.route("/history")
def history():
    return jsonify(list_cases(10))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
