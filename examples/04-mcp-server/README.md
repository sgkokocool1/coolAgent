# 示例 04：最小 MCP 风格 JSON-RPC over stdio

## 目标

演示 MCP 的核心思想：Client 通过统一协议发现 Server 能力，并以结构化方式调用工具。本示例不依赖官方 MCP SDK，而是用标准库实现一个简化版 JSON-RPC over stdio 天气 Tool Server。

## 运行方式

```bash
python client_demo.py
```

如果本机没有 `python` 命令，请使用 `python3 client_demo.py`。

也可以单独启动 Server：

```bash
python server.py
```

单独启动时，Server 会等待标准输入中的 JSON-RPC 请求。

## 核心代码说明

- `server.py` 支持三个方法：
  - `initialize`：返回 Server 信息和能力。
  - `tools/list`：返回 `get_weather` 工具描述。
  - `tools/call`：执行天气工具并返回结构化结果。
- `client_demo.py` 使用 `subprocess.Popen` 启动 Server，并通过 stdin/stdout 发送一行一个 JSON-RPC 消息。
- 这个示例刻意保持简化，重点展示“能力发现”和“工具调用”分离的协议模式。
