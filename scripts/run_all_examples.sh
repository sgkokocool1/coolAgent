#!/usr/bin/env bash
# 冒烟运行全部示例与综合项目
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${PYTHON:-python3}"

run() {
  echo "==== $1 ===="
  (cd "$ROOT/$1" && "$PY" -B "${2:-main.py}")
}

run examples/01-weather-agent
run examples/02-react-agent
run examples/03-langgraph-mini
(cd "$ROOT/examples/04-mcp-server" && "$PY" -B client_demo.py)
run examples/05-skill-registry
run examples/06-context-memory
run examples/07-workflow
run examples/08-tool-calling
run examples/09-slm-router
run examples/10-cache
run examples/11-security
run examples/12-voice-pipeline

run projects/01-weather
run projects/02-search-agent
run projects/03-multi-agent
run projects/04-voice-assistant
run projects/05-enterprise-agent

echo "==== unittest ===="
"$PY" -B -m unittest tests/test_scaffolds.py -v

echo "ALL PASSED"
