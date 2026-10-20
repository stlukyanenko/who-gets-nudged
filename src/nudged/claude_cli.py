"""Inspect model provider that runs Claude models through headless `claude -p`.

His decision 2026-10-18: Claude models run on his subscription through `claude -p`.
Known deviation, disclosed in every write-up: Claude Code adds about 700 tokens of its
own context (identity line, account context, environment). See docs/CLAUDE_P_CHECK.md.

Usage: --model claudecli/claude-haiku-5-5   (optional: -M effort=low)
"""

import asyncio
import json
import tempfile
from pathlib import Path
from typing import Any

from inspect_ai.model import (
    ChatMessage,
    ChatMessageSystem,
    ChatMessageUser,
    GenerateConfig,
    ModelAPI,
    ModelOutput,
    ModelUsage,
    modelapi,
)
from inspect_ai.tool import ToolChoice, ToolInfo

# An empty working directory, so no project CLAUDE.md or files reach the model.
EMPTY_DIR = Path(tempfile.gettempdir()) / "who-gets-nudged-claude-empty"


@modelapi(name="claudecli")
class ClaudeCLIAPI(ModelAPI):
    def __init__(self, model_name: str, base_url: str | None = None, api_key: str | None = None,
                 config: GenerateConfig = GenerateConfig(), **model_args: Any) -> None:
        super().__init__(model_name=model_name, base_url=base_url, api_key=api_key, config=config)
        self.effort = model_args.get("effort")
        self.timeout = float(model_args.get("timeout", 300))
        EMPTY_DIR.mkdir(exist_ok=True)

    def max_connections(self) -> int:
        return 4  # subscription rate limits; raise carefully

    async def generate(self, input: list[ChatMessage], tools: list[ToolInfo],
                       tool_choice: ToolChoice, config: GenerateConfig) -> ModelOutput:
        system = "\n\n".join(m.text for m in input if isinstance(m, ChatMessageSystem))
        users = [m for m in input if isinstance(m, ChatMessageUser)]
        if len(users) != 1 or len(input) != len(users) + (1 if system else 0):
            raise ValueError("claudecli supports one system message and one user message only")
        cmd = ["claude", "-p", users[0].text, "--model", self.model_name,
               "--tools", "", "--strict-mcp-config", "--output-format", "json"]
        if system:
            cmd += ["--system-prompt", system]
        if self.effort:
            cmd += ["--effort", str(self.effort)]
        proc = await asyncio.create_subprocess_exec(
            *cmd, cwd=EMPTY_DIR, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        out, err = await asyncio.wait_for(proc.communicate(), timeout=self.timeout)
        events = json.loads(out.decode())
        result = next(e for e in events if e.get("type") == "result")
        if result.get("is_error"):
            raise RuntimeError(f"claude -p error: {result.get('result')!r}")
        u = result.get("usage", {})
        input_tokens = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
        output = ModelOutput.from_content(model=self.model_name, content=result.get("result", ""))
        output.usage = ModelUsage(
            input_tokens=input_tokens,
            output_tokens=u.get("output_tokens", 0),
            total_tokens=input_tokens + u.get("output_tokens", 0),
            reasoning_tokens=(u.get("output_tokens_details") or {}).get("thinking_tokens"),
        )
        return output
