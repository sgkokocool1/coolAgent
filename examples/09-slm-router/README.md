# 示例 09：SLM Router

本示例演示如何根据请求特征路由到不同模型：

- `mock_local_slm`：端侧小模型，低延迟、低成本、隐私友好。
- `mock_cloud_gpt`：低成本云模型。
- `mock_claude`：强推理云模型。

决策维度：

- 文本复杂度。
- 隐私关键词。
- 延迟预算。
- 成本预算。

运行：

```bash
python main.py
```

默认不需要 API Key。可以设置 `USE_REAL_CLOUD_MODEL=1` 观察真实云模型开关路径：

```bash
USE_REAL_CLOUD_MODEL=1 python main.py
```

示例仍会返回 Mock 结果，真实接入时应在 `mock_cloud_gpt` 和 `mock_claude` 中调用对应 SDK。
