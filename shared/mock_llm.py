"""A tiny local LLM replacement used by the tutorial examples.

The examples default to :class:`MockLLM` so they can run without network access
or API keys. Set ``LLM_PROVIDER=openai`` and ``OPENAI_API_KEY`` to try the
OpenAI-compatible adapter against a real endpoint.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Iterable


Message = dict[str, Any]
ToolCall = dict[str, Any]
ChatResult = dict[str, Any]


def _last_user_message(messages: Iterable[Message]) -> str:
    for message in reversed(list(messages)):
        if message.get("role") == "user":
            return str(message.get("content", ""))
    return ""


def _normalize_tool_names(tools: Any) -> set[str]:
    if not tools:
        return set()

    names: set[str] = set()
    for tool in tools:
        if isinstance(tool, str):
            names.add(tool)
            continue

        if not isinstance(tool, dict):
            continue

        if "name" in tool:
            names.add(str(tool["name"]))
        function = tool.get("function")
        if isinstance(function, dict) and "name" in function:
            names.add(str(function["name"]))
    return names


def _tool_call(name: str, arguments: dict[str, Any]) -> ToolCall:
    return {
        "id": f"call_{name}",
        "type": "function",
        "function": {
            "name": name,
            "arguments": json.dumps(arguments, ensure_ascii=False),
        },
    }


class MockLLM:
    """Keyword-based chat model with minimal function-calling support."""

    def chat(self, messages: list[Message], tools: Any | None = None) -> ChatResult:
        user_text = _last_user_message(messages)
        tool_names = _normalize_tool_names(tools)

        if tool_names:
            calls = self._select_tool_calls(user_text, tool_names)
            if calls:
                return {"role": "assistant", "content": "", "tool_calls": calls}

        return {"role": "assistant", "content": self._answer(user_text)}

    def _select_tool_calls(self, text: str, tool_names: set[str]) -> list[ToolCall]:
        lowered = text.lower()
        calls: list[ToolCall] = []

        if "get_weather" in tool_names and any(word in lowered for word in ["天气", "weather", "温度"]):
            calls.append(_tool_call("get_weather", {"city": self._extract_city(text)}))

        if "calculator" in tool_names and any(word in lowered for word in ["计算", "calculate", "+", "-", "*", "/", "平方"]):
            expression = self._extract_expression(text)
            calls.append(_tool_call("calculator", {"expression": expression}))

        return calls

    def _answer(self, text: str) -> str:
        lowered = text.lower()
        if "react" in lowered:
            return "ReAct 将推理拆成 Thought、Action、Observation，并在观察结果后继续决策。"
        if "mcp" in lowered:
            return "MCP 通过统一协议连接模型应用与工具、资源、提示模板，降低集成成本。"
        if "天气" in text or "weather" in lowered:
            return "我可以通过天气工具查询城市天气。"
        if "计算" in text or "calculate" in lowered:
            return "我可以通过 calculator 工具执行简单算术。"
        return "这是一个本地 MockLLM 回复：我会根据关键词模拟 Agent 决策。"

    def _extract_city(self, text: str) -> str:
        known_cities = ["北京", "上海", "广州", "深圳", "杭州", "成都", "纽约", "伦敦"]
        for city in known_cities:
            if city in text:
                return city

        match = re.search(r"(?:in|for)\s+([A-Za-z][A-Za-z\s-]{1,30})", text)
        if match:
            return match.group(1).strip()

        return "北京"

    def _extract_expression(self, text: str) -> str:
        text = text.replace("乘以", "*").replace("除以", "/").replace("加", "+").replace("减", "-")
        match = re.search(r"[-+*/().\d\s]{3,}", text)
        if match:
            return match.group(0).strip()
        if "平方" in text:
            number = re.search(r"\d+(?:\.\d+)?", text)
            if number:
                value = number.group(0)
                return f"{value} * {value}"
        return "1 + 1"


@dataclass
class OpenAICompatibleLLM:
    """Small OpenAI-compatible chat client using only the Python standard library."""

    model: str = "gpt-4o-mini"
    base_url: str = "https://api.openai.com/v1"
    api_key: str | None = None

    def chat(self, messages: list[Message], tools: Any | None = None) -> ChatResult:
        api_key = self.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }
        if tools:
            payload["tools"] = tools

        request = urllib.request.Request(
            url=f"{self.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI-compatible request failed: {exc.code} {body}") from exc

        return data["choices"][0]["message"]


def create_llm() -> MockLLM | OpenAICompatibleLLM:
    """Create the configured chat model.

    Defaults to MockLLM. To call a real OpenAI-compatible endpoint:

    ``LLM_PROVIDER=openai OPENAI_API_KEY=... OPENAI_BASE_URL=... python3 main.py``
    """

    if os.getenv("LLM_PROVIDER", "").lower() == "openai":
        return OpenAICompatibleLLM(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        )
    return MockLLM()
