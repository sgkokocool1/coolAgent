# 示例 02：完整 ReAct 循环

## 目标

演示 ReAct 的 `Thought -> Action -> Observation` 闭环。Agent 会根据用户任务先查询天气，再执行计算，最后综合观察结果输出答案。

## 运行方式

```bash
python main.py
```

如果本机没有 `python` 命令，请使用 `python3 main.py`。

## 核心代码说明

- `ReActAgent.run()` 控制最大循环步数，避免无限思考。
- `plan_next_step()` 生成下一步 Thought 和 Action。
- `invoke_tool()` 根据 Action 调用 `get_weather` 或 `calculator`。
- 每次工具返回值都会作为 Observation 写入 `ReActState.observations`。
- `calculator()` 使用 Python `ast` 白名单解析，只允许基础四则运算，避免直接 `eval` 的安全风险。
