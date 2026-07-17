from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from shared import create_llm


WEATHER_DATA = {
    "北京": {"condition": "晴", "temperature": 28, "wind": "东北风 2 级"},
    "上海": {"condition": "多云", "temperature": 30, "wind": "东南风 3 级"},
    "杭州": {"condition": "小雨", "temperature": 26, "wind": "北风 2 级"},
    "深圳": {"condition": "阵雨", "temperature": 31, "wind": "南风 3 级"},
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的模拟天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称，例如北京"},
                },
                "required": ["city"],
            },
        },
    }
]


def get_weather(city: str) -> dict[str, Any]:
    weather = WEATHER_DATA.get(city, {"condition": "未知", "temperature": None, "wind": "未知"})
    return {"city": city, **weather}


def parse_arguments(raw_arguments: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(raw_arguments, dict):
        return raw_arguments
    return json.loads(raw_arguments or "{}")


def run_weather_agent(question: str) -> str:
    llm = create_llm()
    messages = [
        {"role": "system", "content": "你是一个天气 Agent。需要天气数据时调用 get_weather。"},
        {"role": "user", "content": question},
    ]

    first_response = llm.chat(messages, tools=TOOLS)
    tool_calls = first_response.get("tool_calls") or []

    if not tool_calls:
        return str(first_response.get("content", "没有生成回复"))

    observations: list[dict[str, Any]] = []
    for call in tool_calls:
        function = call["function"]
        if function["name"] != "get_weather":
            continue
        arguments = parse_arguments(function.get("arguments", "{}"))
        observations.append(get_weather(str(arguments.get("city", "北京"))))

    if not observations:
        return "没有可用的天气工具结果。"

    weather = observations[0]
    if weather["temperature"] is None:
        return f"{weather['city']}暂时没有模拟天气数据，风况：{weather['wind']}。"

    return (
        f"{weather['city']}当前天气：{weather['condition']}，"
        f"{weather['temperature']}℃，{weather['wind']}。"
        "如果要外出，建议结合体感温度和降雨情况安排。"
    )


def main() -> None:
    question = "北京今天天气怎么样？适合出门散步吗？"
    print("用户：", question)
    print("Agent：", run_weather_agent(question))


if __name__ == "__main__":
    main()
