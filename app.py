from functools import partial
from secrets import compare_digest

from flask import Flask, abort, jsonify, render_template, request
from psutil import Error as PsutilError

from config import AUTH_PASSWORD, SEND_LOGS_TO_LLM
from agents.monitor import get_system_status
from agents.log_agent import analyze_logs
from agents.reasoning_agent import reason
from agents.action_agent import act
from core.llm import call_llm
from core.memory import save_case, list_cases

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
app.config["AUTOOPS_AUTH_PASSWORD"] = AUTH_PASSWORD


@app.before_request
def require_authentication():
    if request.endpoint is None:
        return

    password = app.config["AUTOOPS_AUTH_PASSWORD"]
    if not password:
        return jsonify(error="Set AUTOOPS_AUTH_PASSWORD to enable access"), 503

    auth = request.authorization
    if (
        auth is None
        or auth.type != "basic"
        or auth.username != "autoops"
        or not compare_digest((auth.password or "").encode(), password.encode())
    ):
        return (
            jsonify(error="Authentication required"),
            401,
            {"WWW-Authenticate": 'Basic realm="AutoOps", charset="UTF-8"'},
        )


@app.after_request
def protect_response(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Frame-Options"] = "DENY"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/run")
def run():
    if request.headers.get("X-AutoOps-Request") != "1":
        abort(403)

    try:
        status = get_system_status()
    except (OSError, PsutilError):
        return jsonify(error="System status unavailable"), 503

    log_analysis = analyze_logs(partial(call_llm, allow_remote=SEND_LOGS_TO_LLM))
    reasoning = reason(status, log_analysis, call_llm)
    action = act(reasoning, partial(call_llm, use_fallback=False))

    case = {
        "status": status,
        "analysis": log_analysis,
        "reasoning": reasoning,
        "action": action
    }
    try:
        save_case(case)
    except (OSError, ValueError):
        app.logger.error("Could not save analysis history")
        return jsonify(error="Analysis completed but could not be saved"), 503

    return jsonify(case)


@app.route("/history")
def history():
    try:
        return jsonify(list_cases(10))
    except (OSError, ValueError):
        app.logger.error("Could not read analysis history")
        return jsonify(error="Analysis history unavailable"), 503


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
