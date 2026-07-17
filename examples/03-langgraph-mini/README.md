# 示例 03：不依赖 LangGraph 的最小图状态机

## 目标

用纯 Python 实现一个极简 `Graph / Node / Edge / State` Agent，演示 LangGraph 的核心思想：节点读取并更新状态，边根据条件决定下一步节点。

## 运行方式

```bash
python main.py
```

如果本机没有 `python` 命令，请使用 `python3 main.py`。

## 核心代码说明

- `MiniGraph` 保存节点、边、入口节点和结束节点。
- `State` 是一个普通字典，贯穿整个图执行过程。
- `parse_intent` 判断是否需要天气工具。
- `call_weather_tool` 写入天气观察结果。
- `generate_answer` 基于最终状态生成回答。

这个示例不依赖 `langgraph` 包，但能帮助理解为什么复杂 Agent 常用图来表达循环、分支和状态更新。
