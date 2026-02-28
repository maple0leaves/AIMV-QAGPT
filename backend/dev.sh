#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR" || exit

PORT="${PORT:-8080}"
HOST="${HOST:-0.0.0.0}"

if [[ "${SHOW_OLLAMA_TIPS:-true}" == "true" ]]; then
  echo "Tip: start Ollama with tuned defaults via ./dev-ollama.sh"
fi

exec uvicorn open_webui.main:app --port "$PORT" --host "$HOST" --forwarded-allow-ips '*' --reload
