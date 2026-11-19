# Security and robustness audit

Locations refer to the original tracked files. The `.gitignore` entry points to the new file. The tracked tree contained no suspected credentials, CI workflows, or binary build outputs. `config.py` already loaded the OpenAI API key from the environment.

| Severity | Location | One-line risk | Fix applied |
| --- | --- | --- | --- |
| high | `app.py:37` | Starting the app exposed the Flask debugger and exception details on all interfaces. | Disabled debug mode and bound the built-in server to loopback. |
| high | `core/executor.py:5` | Enabling auto-execution passed model-generated text from the analysis chain to a shell. | Limited execution to fixed argument vectors for read-only diagnostics, with a timeout and no shell. |
| high | `app.py:15` | Unauthenticated callers could run analysis, consume the operator’s LLM quota, and write to history. | Required HTTP Basic authentication with an operator-configured password and denied access when unset. |
| high | `app.py:32` | Unauthenticated callers could read stored host metrics, analysis, and command results. | Required authentication and set `Cache-Control: no-store` for responses. |
| medium | `app.py:15` | The state-changing GET could be triggered by cross-site navigation or a prefetch. | Required POST and a custom request header. Denied framing to protect the dashboard controls. |
| medium | `agents/log_agent.py:15` | Configuring an LLM key silently sent raw operational logs to a third party. | Kept raw log analysis local by default and documented explicit opt-in for remote log analysis. |
| medium | `agents/log_agent.py:6` | Every analysis read the entire log file into memory and suppressed decoding failures. | Bounded reads to the newest 32 KiB and 50 lines, with replacement decoding for malformed text. |
| medium | `core/memory.py:15` | Concurrent writers could lose records, and a reader or interruption could observe a partially written history file. | Serialized writers with a file lock and atomically replaced history with a private, flushed file. |
| medium | `core/memory.py:11` | A failed history read was treated as empty before overwriting the original data. | Preserved unreadable or invalid history and returned a controlled service error. |
| medium | `core/llm.py:28` | An upstream redirect could cause the HTTP client to resend a prompt to another destination. | Disabled redirects and required a successful response from the fixed API endpoint. |
| medium | `core/llm.py:30` | Invalid provider output could break later steps, and raw exception text could appear in responses or stored cases. | Validated response content and used generic logging and local fallback for expected failures. |
| medium | `requirements.txt:1` | Unpinned dependencies allowed known-vulnerable versions, including Requests 2.31.0 in the audit environment. | Pinned direct dependencies and Jinja2, urllib3, and Werkzeug to reviewed releases. [Requests advisory](https://github.com/advisories/GHSA-9hjg-9r4m-mvj7), [Flask release](https://github.com/pallets/flask/releases/tag/3.1.3), [urllib3 advisory](https://github.com/urllib3/urllib3/security/advisories/GHSA-vxq7-64xx-v4gw), [Werkzeug release](https://github.com/pallets/werkzeug/releases/tag/3.1.9). |
| low | `agents/action_agent.py:11` | Empty model output could crash analysis, and fallback prose could be presented as a command. | Returned an explicit no-command result and disabled the general-purpose fallback for command generation. |
| low | `core/llm.py:9` | The fallback reported high CPU whenever the metric name appeared, regardless of the measurement. | Removed the unsupported diagnosis and used qualified wording for 502-related text. |
| low | `web/templates/index.html:18` | Failed HTTP requests gave no clear feedback, and the history handler shared a name with a browser global. | Attached explicit click handlers and displayed HTTP and fetch failures as text. |
| low | `app.py:17` | A host metric I/O failure produced an unhandled server error. | Returned a controlled service-unavailable response for expected monitoring failures. |
| low | `logs/system.log:1` | Versioning the default runtime log path could expose operational data in future diffs. | Removed the tracked copy in the working tree and ignored runtime logs. |
| low | `.gitignore:1` | Environment files, analysis history, and local artifacts could be committed accidentally. | Added ignore rules and an environment template containing empty credential fields. |
| low | `requirements.txt:1` | Unpinned transitive dependencies still make installations non-reproducible. | Report-only. The shell could not access the package index to resolve and verify a complete hashed lockfile. |
| low | `core/memory.py:14` | History grows without a retention limit, so storage and rewrite cost increase over time. | Report-only. A retention limit would discard existing saved cases and needs a retention policy. |

Python and JavaScript syntax checks passed. Local tests covered command rejection, provider failures, bounded log reads, concurrent history writes, recovery from write failures, and dashboard request handling. Authentication and endpoint logic passed handler tests with stubs. Full Flask integration was unavailable because Flask and psutil were absent and the shell could not access the package index.
