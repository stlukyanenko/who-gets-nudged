#!/usr/bin/env zsh -i
# Generate answers for all 420 cells on all 6 models (exploratory run v1).
# Run with: zsh -i src/run_generation.sh <log-dir>   (interactive zsh loads OPENROUTER_API_KEY)
# Claude models run one after another (subscription rate limits); OpenRouter models run in parallel.
set -u
LOGDIR=${1:-logs/full_v1}
cd "$(dirname "$0")/.."
mkdir -p "$LOGDIR"
echo "claude CLI: $(claude --version)" | tee "$LOGDIR/versions.txt"
uv run python -c "import inspect_ai; print('inspect_ai', inspect_ai.__version__)" | tee -a "$LOGDIR/versions.txt"

run() {  # model, provider-json (or empty)
  local extra=()
  [[ -n "$2" ]] && extra=(--reasoning-effort none -M "provider=$2")
  uv run inspect eval src/nudged/task.py --model "$1" --log-dir "$LOGDIR" --display plain \
    --retry-on-error 3 "${extra[@]}" > "$LOGDIR/$(echo $1 | tr '/' '_').out" 2>&1
  echo "done: $1 (exit $?)"
}

run openrouter/qwen/qwen3.8-27b '{"order": ["deepinfra/bf16"], "allow_fallbacks": false}' &
run openrouter/openai/gpt-6-luna '{"order": ["azure"], "allow_fallbacks": false}' &
run openrouter/mistralai/mistral-small-2603 '{"order": ["mistral"], "allow_fallbacks": false}' &
for m in claude-haiku-5-5 claude-sonnet-5-5 claude-opus-5-5; do
  run claudecli/$m ''
done
wait
echo "all done"
