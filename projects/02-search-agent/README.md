# 项目 02：ReAct + Memory + 假搜索/RAG

## 项目目标

构建一个能展示 ReAct 推理轨迹的搜索 Agent：先产生 Thought，再执行假搜索 Action，读取 Observation，最后结合 Memory 输出 Final。

## 运行

```bash
python3 projects/02-search-agent/main.py
```

## 任务说明

1. 阅读 `DOCUMENTS`，理解假 RAG 语料如何被关键词命中。
2. 在 `FakeSearch.search()` 中加入更细的打分规则，例如标题命中加分、正文命中加分。
3. 扩展 `Memory`，区分用户偏好、长期事实和本轮中间结论。
4. 将 `ReActAgent.ask()` 拆成多步循环，允许一次问题调用多次搜索。
5. 替换假搜索为真实搜索 API 或向量数据库时，保持 `search(query) -> list[str]` 接口。

## 验收标准

- 运行脚本后能看到 Thought、Action、Observation、Final。
- 第二轮回答能展示上一轮写入的记忆。
- 无网络环境下输出稳定。
- 扩展文档库后，问题命中新文档时能进入 Observation。
