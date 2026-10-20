#!/usr/bin/env zsh -i
# Score every generation log in <log-dir> with the three judges (one judge per pass,
# scores appended to the log, so each log ends up with three score columns).
# Run with: zsh -i src/run_judges.sh <log-dir> [file-with-log-paths]
# (the optional second argument limits judging to the listed logs)
set -u
LOGDIR=${1:-logs/full_v1}
cd "$(dirname "$0")/.."
if [[ $# -ge 2 ]]; then LOGS=("${(@f)$(<$2)}"); else LOGS=("$LOGDIR"/*.eval); fi

judge() {  # log, judge model, extra -S args...
  local log=$1 model=$2; shift 2
  uv run inspect score "$log" --scorer src/nudged/judge.py@darkbench_judge \
    -S judge_model="$model" "$@" --action append --overwrite --display plain \
    >> "$LOGDIR/judges.out" 2>&1
  echo "scored $(basename $log) with $model (exit $?)"
}

for log in "${LOGS[@]}"; do
  judge "$log" openrouter/google/gemini-3.8-flash -S reasoning_effort=low
  judge "$log" openrouter/openai/gpt-6-luna -S reasoning_effort=low \
    -S 'provider={"order": ["azure"], "allow_fallbacks": false}'
  judge "$log" claudecli/claude-sonnet-5-5
done
echo "all judged"
