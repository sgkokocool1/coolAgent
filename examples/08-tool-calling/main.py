from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Callable


ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: ToolHandler


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"工具已注册：{tool.name}")
        self._tools[tool.name] = tool

    def list_schemas(self) -> list[dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            }
            for tool in self._tools.values()
        ]

    def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if name not in self._tools:
            raise ValueError(f"未注册工具：{name}")
        tool = self._tools[name]
        validate_arguments(tool.parameters, arguments)
        return tool.handler(arguments)


def validate_arguments(schema: dict[str, Any], arguments: dict[str, Any]) -> None:
    if schema.get("type") != "object":
        raise ValueError("示例校验器只支持 object schema")

    properties = schema.get("properties", {})
    required = schema.get("required", [])

    for field in required:
        if field not in arguments:
            raise ValueError(f"缺少必填参数：{field}")

    for field, value in arguments.items():
        if field not in properties:
            raise ValueError(f"未知参数：{field}")
        expected = properties[field].get("type")
        if expected == "string" and not isinstance(value, str):
            raise ValueError(f"参数 {field} 应为 string")
        if expected == "number" and not isinstance(value, (int, float)):
            raise ValueError(f"参数 {field} 应为 number")
        if expected == "boolean" and not isinstance(value, bool):
            raise ValueError(f"参数 {field} 应为 boolean")
        allowed = properties[field].get("enum")
        if allowed and value not in allowed:
            raise ValueError(f"参数 {field} 必须属于 {allowed}")


def get_weather(arguments: dict[str, Any]) -> dict[str, Any]:
    city = arguments["city"]
    unit = arguments.get("unit", "celsius")
    temperature = 26 if unit == "celsius" else 79
    return {
        "city": city,
        "condition": "多云",
        "temperature": temperature,
        "unit": unit,
    }


def calculate(arguments: dict[str, Any]) -> dict[str, Any]:
    left = float(arguments["left"])
    right = float(arguments["right"])
    operator = arguments["operator"]
    operations = {
        "add": left + right,
        "subtract": left - right,
        "multiply": left * right,
        "divide": left / right if right != 0 else None,
    }
    result = operations[operator]
    if result is None:
        return {"error": "除数不能为 0"}
    return {"result": result}


def mock_llm_select_tool(user_message: str, tools: list[dict[str, Any]]) -> dict[str, Any]:
    if os.getenv("USE_REAL_LLM") == "1":
        return {
            "type": "message",
            "content": "真实 LLM 开关已启用；本地示例仍使用安全 Mock 路径。",
        }

    if "天气" in user_message:
        return {
            "type": "tool_call",
            "name": "get_weather",
            "arguments": {"city": "上海", "unit": "celsius"},
        }
    if "乘" in user_message or "*" in user_message:
        return {
            "type": "tool_call",
            "name": "calculate",
            "arguments": {"left": 12, "right": 7, "operator": "multiply"},
        }
    return {
        "type": "message",
        "content": f"当前注册了 {len(tools)} 个工具，但这个问题不需要调用工具。",
    }


def mock_llm_final_answer(user_message: str, tool_name: str, tool_result: dict[str, Any]) -> str:
    if tool_name == "get_weather":
        return (
            f"根据工具结果，{tool_result['city']}当前{tool_result['condition']}，"
            f"温度 {tool_result['temperature']}°C。"
        )
    if tool_name == "calculate":
        if "error" in tool_result:
            return f"计算失败：{tool_result['error']}"
        return f"计算完成：{user_message} 的结果是 {tool_result['result']}。"
    return f"工具 {tool_name} 返回：{json.dumps(tool_result, ensure_ascii=False)}"


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        Tool(
            name="get_weather",
            description="查询指定城市的当前天气，只用于天气问题。",
            parameters={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名"},
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "温度单位",
                    },
                },
                "required": ["city"],
            },
            handler=get_weather,
        )
    )
    registry.register(
        Tool(
            name="calculate",
            description="执行基础四则运算。",
            parameters={
                "type": "object",
                "properties": {
                    "left": {"type": "number"},
                    "right": {"type": "number"},
                    "operator": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                    },
                },
                "required": ["left", "right", "operator"],
            },
            handler=calculate,
        )
    )
    return registry


def run_turn(user_message: str, registry: ToolRegistry) -> str:
    schemas = registry.list_schemas()
    decision = mock_llm_select_tool(user_message, schemas)
    print("模型决策：")
    print(json.dumps(decision, ensure_ascii=False, indent=2))

    if decision["type"] == "message":
        return decision["content"]

    tool_result = registry.execute(decision["name"], decision["arguments"])
    print("工具结果：")
    print(json.dumps(tool_result, ensure_ascii=False, indent=2))
    return mock_llm_final_answer(user_message, decision["name"], tool_result)


def main() -> None:
    registry = build_registry()
    print("已注册工具：")
    print(json.dumps(registry.list_schemas(), ensure_ascii=False, indent=2))

    for message in ["上海今天天气怎么样？", "12 乘 7 等于多少？"]:
        print("\n=== 用户问题 ===")
        print(message)
        answer = run_turn(message, registry)
        print("最终回答：")
        print(answer)


if __name__ == "__main__":
    main()
