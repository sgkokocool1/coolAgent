from __future__ import annotations

import json
import sys
from typing import Any


WEATHER_DATA = {
    "北京": {"condition": "晴", "temperature": 28, "wind": "东北风 2 级"},
    "上海": {"condition": "多云", "temperature": 30, "wind": "东南风 3 级"},
    "杭州": {"condition": "小雨", "temperature": 26, "wind": "北风 2 级"},
}


def jsonrpc_result(request_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def jsonrpc_error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def list_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": "get_weather",
            "description": "查询指定城市的模拟天气",
            "inputSchema": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名称"}},
                "required": ["city"],
            },
        }
    ]


def get_weather(city: str) -> dict[str, Any]:
    weather = WEATHER_DATA.get(city)
    if weather is None:
        return {"city": city, "condition": "未知", "temperature": None, "wind": "未知"}
    return {"city": city, **weather}


def handle_request(request: dict[str, Any]) -> dict[str, Any]:
    request_id = request.get("id")
    method = request.get("method")
    params = request.get("params") or {}

    if method == "initialize":
        return jsonrpc_result(
            request_id,
            {
                "serverInfo": {"name": "mini-weather-mcp", "version": "0.1.0"},
                "capabilities": {"tools": True, "resources": False, "prompts": False},
            },
        )

    if method == "tools/list":
        return jsonrpc_result(request_id, {"tools": list_tools()})

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if name != "get_weather":
            return jsonrpc_error(request_id, -32601, f"未知工具: {name}")
        city = str(arguments.get("city", "北京"))
        return jsonrpc_result(request_id, {"content": [{"type": "json", "json": get_weather(city)}]})

    return jsonrpc_error(request_id, -32601, f"未知方法: {method}")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
        except json.JSONDecodeError as exc:
            response = jsonrpc_error(None, -32700, f"JSON 解析失败: {exc}")
        print(json.dumps(response, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
