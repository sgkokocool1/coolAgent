# 第 18 章：五阶段综合项目任务书

本章把前面章节串成五个递进项目。每个项目在 `projects/` 下都有可运行最小脚手架，学习路径从 Function Calling 到企业端 Agent，再回到语音流水线。

建议顺序：

1. 入门天气 Agent。
2. 联网搜索/RAG Agent。
3. 多 Agent 协作。
4. 语音助手。
5. 企业端云 Agent。

所有项目都可以离线运行，真实 API、真实模型和真实数据库都是后续替换项。

## 阶段一：入门天气 Agent

路径：`projects/01-weather/`

### 目标

掌握 Function Calling 的最小闭环：用户问题 -> 函数调用 -> 工具观察 -> 最终回答。

### 背景

天气查询是最适合入门的工具调用任务：意图清晰、参数少、结果可验证。你不需要真实天气 API，也能理解 Agent 如何把自然语言转成结构化调用。

### 详细任务

1. 运行 `python3 projects/01-weather/main.py`，观察输出。
2. 阅读 `FunctionCall` 数据结构，理解工具名和参数。
3. 在 `WeatherAgent.plan()` 中增加更多城市识别。
4. 为日期增加简单解析：今天、明天、后天。
5. 模拟工具失败，例如城市未知时返回错误。
6. 修改 `WeatherAgent.answer()`，让失败回复更自然。
7. 可选：把假数据替换成真实天气 API。

### 验收标准

- 输出包含函数调用、工具观察和最终回答。
- 至少支持三个城市。
- 工具失败时不会抛出未处理异常。
- 回答是适合语音播报的短中文句子。

### 进阶问题

- 如果用户说“那里天气呢”，如何从上下文补齐城市？
- 如果工具返回摄氏度和华氏度，如何选择用户偏好的单位？
- 如果天气 API 很慢，Agent 应该先说什么？

## 阶段二：联网搜索 + RAG Agent

路径：`projects/02-search-agent/`

### 目标

掌握 ReAct、Memory 和检索增强生成的组合方式。

### 背景

很多 Agent 不能只依赖模型参数知识。它需要搜索网页、查企业知识库或读取文档。ReAct 让过程可解释：Thought 说明为什么查，Action 表示查什么，Observation 保存查到什么，Final 给用户答案。

### 详细任务

1. 运行 `python3 projects/02-search-agent/main.py`。
2. 观察第一轮和第二轮输出，确认 Memory 生效。
3. 向 `DOCUMENTS` 增加三条业务文档。
4. 修改 `FakeSearch.search()`，实现关键词打分和 Top-K。
5. 给 `Memory` 增加分类：偏好、事实、临时观察。
6. 支持一次问题多次检索，例如先查定义，再查最佳实践。
7. 可选：替换成真实搜索 API 或向量数据库。

### 验收标准

- 输出包含 Thought、Action、Observation、Final。
- 第二轮能引用第一轮记忆。
- 检索结果影响最终回答。
- 搜索无结果时有降级回复。

### 进阶问题

- 如何避免把错误搜索结果当成事实？
- Memory 什么时候应该遗忘？
- RAG 文档过长时如何切片和引用来源？

## 阶段三：多 Agent 协作

路径：`projects/03-multi-agent/`

### 目标

掌握多角色协作的基本调度方式：PM 拆需求、Dev 产方案、Tester 验收。

### 背景

多 Agent 不是“多开几个模型”就有价值。关键在于角色边界和交付物格式。每个角色都应有明确输入、输出和验收标准。

### 详细任务

1. 运行 `python3 projects/03-multi-agent/main.py`。
2. 阅读 `Task`，理解 PM 输出的结构化任务。
3. 让 `TesterAgent.review()` 返回列表形式的问题。
4. 增加 Reviewer 角色，检查方案是否过度设计。
5. 增加重试机制：Tester 不通过时 Dev 根据反馈修改。
6. 把每个角色的输出保存到 JSON 事件流。
7. 可选：把角色背后的固定逻辑替换成真实 LLM。

### 验收标准

- 输出包含 PM、Dev、Tester。
- Tester 可以阻止不完整方案通过。
- 新增角色不需要重写所有旧角色。
- 协作过程可追踪。

### 进阶问题

- 多 Agent 什么时候会比单 Agent 更差？
- 如何控制角色之间互相“客套”导致的低效？
- 哪些步骤应该由确定性代码完成，而不是交给模型？

## 阶段四：语音助手

路径：`projects/04-voice-assistant/` 与 `examples/12-voice-pipeline/`

### 目标

掌握语音 Agent 的状态机和 Mock 流水线：Mic -> VAD -> ASR -> LLM -> Tool -> LLM -> TTS -> Speaker。

### 背景

语音助手需要处理实时事件。文本 Agent 可以等待模型完整回复；语音 Agent 必须处理端点、首包延迟、TTS 播放和用户打断。

### 详细任务

1. 运行 `python3 examples/12-voice-pipeline/main.py`，观察完整链路。
2. 运行 `python3 projects/04-voice-assistant/main.py`，观察状态迁移。
3. 修改 `demo_audio_events()`，增加第三轮用户输入。
4. 调整 `MockVAD` 参数，观察端点变化。
5. 修改 `MockTTS.chunk_size`，模拟更细或更粗的流式播报。
6. 在状态机中加入超时状态。
7. 可选：把 Mock ASR/TTS 替换成真实模型适配器。

### 验收标准

- 能看到 Mic、VAD、ASR、Tool、LLM、TTS 日志。
- 第一轮播报可以被打断。
- 打断后新意图继续完成。
- 状态机最终回到空闲。

### 进阶问题

- 用户说“等等”后没有继续说，系统应该怎么做？
- 播报期间如何避免 TTS 被 ASR 识别成用户语音？
- 低置信度 ASR 结果应该追问还是直接执行？

## 阶段五：企业端云 Agent

路径：`projects/05-enterprise-agent/`

### 目标

掌握企业 Agent 的四个骨架：模型路由、技能注册、权限控制和工作流。

### 背景

企业 Agent 的难点不只是回答问题，而是安全地执行业务动作。它必须知道谁在请求、能访问什么数据、能执行什么技能、每一步是否可审计。

### 详细任务

1. 运行 `python3 projects/05-enterprise-agent/main.py`。
2. 阅读 `SLMRouter`，理解按意图选择模型。
3. 将 `SkillRegistry` 改成动态注册。
4. 为 `PermissionGuard` 增加数据范围，例如部门和金额。
5. 在 `WorkflowEngine.handle()` 中记录审计日志。
6. 增加人工审批节点，高风险动作不直接执行。
7. 可选：接入真实 SSO、工单系统和知识库。

### 验收标准

- 普通查询走小模型或 RAG 模型。
- 审批类动作检查权限。
- 权限不足时拒绝执行并给出中文原因。
- 技能调用结果进入最终回复。
- 每次高风险动作都可审计。

### 进阶问题

- 如何防止 Prompt Injection 诱导 Agent 越权？
- 模型路由按成本、延迟还是准确率优先？
- 企业知识库结果如何做权限过滤？

## 总体验收

完成五阶段后，应能做到：

- 清楚解释 Function Calling、ReAct、Memory、多 Agent、语音状态机和企业工作流的区别。
- 能运行所有项目脚手架。
- 能把 Mock 工具替换成真实 API，同时保持 Agent 接口稳定。
- 能设计可打断的语音 Agent。
- 能说明企业场景为什么必须有权限、审计和降级策略。

推荐最终验证命令：

```bash
python3 examples/12-voice-pipeline/main.py
python3 projects/01-weather/main.py
python3 projects/02-search-agent/main.py
python3 projects/03-multi-agent/main.py
python3 projects/04-voice-assistant/main.py
python3 projects/05-enterprise-agent/main.py
```
