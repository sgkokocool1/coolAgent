# 示例 07：线性 Workflow 编排器

本示例演示一个自实现的线性 Workflow：

```text
Start -> Tool -> LLM -> Tool -> End
```

特点：

- 使用 Python 3.11+ 标准库。
- 默认使用 Mock LLM，不需要 API Key。
- 通过 `USE_REAL_LLM=1` 预留真实 API 接入开关，但示例不会主动发起外部请求。
- 每个节点都会写入时间线，便于观察执行过程。

运行：

```bash
python main.py
```

你可以尝试修改 `main.py` 中的 `user_request`，观察计划节点选择的 `intent` 如何变化。
