"""Inspect task for "Who gets nudged" (docs/DESIGN.md).

Each sample is one cell from src/data/cells.jsonl (built by src/build_prompts.py):
a company system prompt plus one user message. This task only generates answers;
judging is a separate step.

Examples:
  inspect eval src/nudged/task.py --model claudecli/claude-haiku-5-5 -T limit=5
  inspect eval src/nudged/task.py --model openrouter/qwen/qwen3.8-27b \
      -M "provider={'order': ['deepinfra/bf16'], 'allow_fallbacks': false}"
"""

import json
from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.dataset import MemoryDataset, Sample
from inspect_ai.model import ChatMessageSystem, ChatMessageUser
from inspect_ai.solver import generate

from nudged import claude_cli  # noqa: F401  registers the claudecli/ provider

CELLS = Path(__file__).resolve().parents[1] / "data" / "cells.jsonl"
META = ("block", "item_id", "category", "cue_type", "base_variant", "deployer", "signal", "sha256")


def load_cells(ids=None, limit=None):
    rows = [json.loads(line) for line in CELLS.read_text().splitlines() if line.strip()]
    if ids:
        wanted = set(ids)
        rows = [r for r in rows if r["cell_id"] in wanted]
    if limit:
        rows = rows[: int(limit)]
    return [
        Sample(
            id=r["cell_id"],
            input=[ChatMessageSystem(content=r["system_prompt"]), ChatMessageUser(content=r["user_message"])],
            metadata={k: r[k] for k in META},
        )
        for r in rows
    ]


@task
def who_gets_nudged(cells_file: str | None = None, limit: int | None = None):
    ids = None
    if cells_file:
        path = Path(cells_file)
        if not path.is_absolute():  # Inspect runs tasks from the task's folder
            path = Path(__file__).resolve().parents[2] / path
        ids = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    return Task(dataset=MemoryDataset(load_cells(ids, limit)), solver=generate())
