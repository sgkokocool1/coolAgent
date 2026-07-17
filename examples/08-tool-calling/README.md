# 示例 08：JSON Schema Tool Calling

本示例演示 Tool Calling 的完整闭环：

1. 注册工具及 JSON Schema 风格参数定义。
2. Mock LLM 根据用户问题选择工具。
3. 运行时校验参数。
4. 执行 Python 工具函数。
5. 把工具结果交回 Mock LLM 生成最终回答。

运行：

```bash
python main.py
```

默认不需要 API Key。可以设置 `USE_REAL_LLM=1` 观察真实模型开关路径：

```bash
USE_REAL_LLM=1 python main.py
```

示例不会主动调用外部模型，真实接入时应把 `mock_llm_select_tool` 替换为厂商 SDK 调用，并保留参数校验和权限检查。
