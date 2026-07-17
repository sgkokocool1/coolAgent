# 示例 06：Sliding Window + Summary Memory

## 目标

演示上下文管理中的两种基础策略：最近消息保留在 Sliding Window 中，更早消息压缩进 Summary Memory。这样可以避免对话历史无限增长，同时保留关键约束。

## 运行方式

```bash
python main.py
```

如果本机没有 `python` 命令，请使用 `python3 main.py`。

## 核心代码说明

- `SlidingSummaryMemory.window` 保存最近 `window_size` 条消息。
- `compact_if_needed()` 在窗口超限时取出最早消息。
- `merge_summary()` 将被移出窗口的消息合并进摘要。
- `build_context()` 构造最终给 LLM 的上下文：先放历史摘要，再放最近窗口。

示例会模拟 6 轮对话，并在每轮后打印 Summary、Window 和最终 Context。
