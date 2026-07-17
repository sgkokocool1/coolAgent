# 示例 01：Function Calling 天气 Agent

## 目标

演示最小 Function Calling Agent：用户提出天气问题，LLM 根据工具描述选择 `get_weather`，Agent 执行本地 Mock 天气 API，并把结果组织成中文回复。

默认使用本地 `MockLLM`，无需 API Key。若要尝试真实 OpenAI 兼容接口，可设置：

```bash
LLM_PROVIDER=openai OPENAI_API_KEY=你的_key OPENAI_BASE_URL=https://api.openai.com/v1 python main.py
```

## 运行方式

```bash
python main.py
```

如果本机没有 `python` 命令，请使用 `python3 main.py`。

## 核心代码说明

- `TOOLS` 定义 OpenAI Function Calling 风格工具 schema。
- `get_weather(city)` 是本地模拟天气 API。
- `run_weather_agent(question)` 先请求 LLM 选择工具，再解析 `tool_calls`，最后生成自然语言答案。
- `shared.MockLLM` 会根据“天气”等关键词自动返回 `get_weather` 工具调用。
