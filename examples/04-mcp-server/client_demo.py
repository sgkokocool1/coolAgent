from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class StdioJsonRpcClient:
    def __init__(self, server_path: Path) -> None:
        self.next_id = 1
        self.process = subprocess.Popen(
            [sys.executable, str(server_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def request(self, method: str, params: dict[str, Any] | None = None) -> Any:
        if self.process.stdin is None or self.process.stdout is None:
            raise RuntimeError("MCP Server 管道未打开")

        request_id = self.next_id
        self.next_id += 1
        payload = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}}
        self.process.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.process.stdin.flush()

        line = self.process.stdout.readline()
        if not line:
            stderr = self.process.stderr.read() if self.process.stderr else ""
            raise RuntimeError(f"MCP Server 没有返回响应: {stderr}")

        response = json.loads(line)
        if "error" in response:
            raise RuntimeError(response["error"]["message"])
        return response["result"]

    def close(self) -> None:
        if self.process.stdin:
            self.process.stdin.close()
        self.process.terminate()
        try:
            self.process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.process.kill()


def main() -> None:
    server_path = Path(__file__).with_name("server.py")
    client = StdioJsonRpcClient(server_path)
    try:
        init = client.request("initialize")
        print("Initialize:", json.dumps(init, ensure_ascii=False))

        tools = client.request("tools/list")
        print("Tools:", json.dumps(tools, ensure_ascii=False))

        result = client.request("tools/call", {"name": "get_weather", "arguments": {"city": "北京"}})
        print("Tool Result:", json.dumps(result, ensure_ascii=False))
    finally:
        client.close()


if __name__ == "__main__":
    main()
