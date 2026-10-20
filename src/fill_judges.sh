#!/usr/bin/env zsh -i
# Add any judge that is still missing from each complete log in <log-dir> (idempotent).
# Run with: zsh -i src/fill_judges.sh <log-dir>
set -u
LOGDIR=${1:-logs/full_v1}
cd "$(dirname "$0")/.."
JUDGES=(openrouter/google/gemini-3.8-flash openrouter/openai/gpt-6-luna claudecli/claude-sonnet-5-5)

for log in "$LOGDIR"/*.eval; do
  missing=$(uv run python - "$log" <<'EOF'
import sys
from inspect_ai.log import read_eval_log
log = read_eval_log(sys.argv[1])
if log.status != "success" or not log.samples:
    sys.exit()
have = {sc.metadata.get("judge") for s in log.samples[:1] for sc in (s.scores or {}).values() if sc.metadata}
for j in ["openrouter/google/gemini-3.8-flash", "openrouter/openai/gpt-6-luna", "claudecli/claude-sonnet-5-5"]:
    if j not in have:
        print(j)
EOF
)
  for j in ${(f)missing}; do
    extra=()
    [[ $j == *gemini* ]] && extra=(-S reasoning_effort=low)
    [[ $j == *luna* ]] && extra=(-S reasoning_effort=low -S 'provider={"order": ["azure"], "allow_fallbacks": false}')
    uv run inspect score "$log" --scorer src/nudged/judge.py@darkbench_judge -S judge_model="$j" "${extra[@]}" \
      --action append --overwrite --display plain >> "$LOGDIR/judges.out" 2>&1
    echo "filled $(basename $log) with $j (exit $?)"
  done
done
echo "fill done"
