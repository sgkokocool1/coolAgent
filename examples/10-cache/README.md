# 示例 10：Prompt Cache 与 Semantic Cache

本示例演示两类缓存：

- Prompt Cache：对规范化后的 Prompt 做精确匹配。
- Semantic Cache：使用 Python 标准库 `difflib.SequenceMatcher` 计算字符串相似度。

运行：

```bash
python main.py
```

默认不需要 API Key。可以设置 `USE_REAL_LLM=1` 观察真实模型开关路径：

```bash
USE_REAL_LLM=1 python main.py
```

真实生产环境中，可以把：

- `PromptCache` 的字典替换为 Redis。
- `SemanticCache` 的字符串相似度替换为 Embedding + 向量数据库。
- 缓存键扩展为包含 `tenant_id`、`user_id`、模型版本和 Prompt 模板版本。
