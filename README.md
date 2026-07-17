# coolAgent · AI Agent 框架与语音 Agent 技术学习路线

掌握主流 AI Agent 架构、框架、MCP、Skill、端云协同与语音 Agent 全链路，最终能独立设计并开发具备多工具调用、上下文管理、工作流编排与语音交互能力的智能 Agent 系统。

## 学习目标

| 能力 | 说明 |
|------|------|
| 独立开发 AI Agent | 理解推理闭环，能写 Tool Calling / ReAct / Workflow Agent |
| 设计 MCP Tool / Skill | 标准化工具协议与业务能力封装 |
| 构建端云协同 Agent | SLM Router、成本与隐私路由 |
| 实现语音 Agent | VAD → ASR → LLM → Tool → TTS |
| 理解企业级架构 | 安全、缓存、权限、编排、审计 |

## 仓库结构

```text
coolAgent/
├── docs/chapters/          # 18 章详细教程
├── examples/               # 12 个可运行示例（默认 Mock，无需 API Key）
├── projects/               # 5 个递进综合项目脚手架
├── shared/                 # MockLLM、语音 Mock 等公共模块
└── tests/                  # 脚手架冒烟测试
```

## 快速开始

```bash
# 建议 Python 3.11+
cd coolAgent

# 绝大多数示例零依赖，直接运行：
python3 examples/01-weather-agent/main.py
python3 examples/02-react-agent/main.py
python3 examples/12-voice-pipeline/main.py

# 综合项目
python3 projects/01-weather/main.py
python3 projects/05-enterprise-agent/main.py

# 可选：冒烟测试
python3 -m unittest tests/test_scaffolds.py -v
```

如需对接真实大模型（OpenAI 兼容接口）：

```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-xxx
export OPENAI_BASE_URL=https://api.openai.com/v1   # 可选
```

## 推荐学习顺序（6 周）

| 周次 | 内容 | 文档 | 实践 |
|------|------|------|------|
| 第 1 周 | LLM 基础、Function Calling、ReAct、OODA、Prompt | [01](docs/chapters/01-agent-basics.md) [02](docs/chapters/02-reasoning-patterns.md) | `examples/01` `02` |
| 第 2 周 | LangGraph / CrewAI / Smolagents / AutoGen | [03](docs/chapters/03-agent-frameworks.md) | `examples/03` + `projects/01` |
| 第 3 周 | MCP、Skill、Tool Calling、Workflow、Context | [04](docs/chapters/04-mcp.md)–[08](docs/chapters/08-tool-calling.md) | `examples/04`–`08` |
| 第 4 周 | RAG、Memory、缓存、SLM Router、端云、安全 | [06](docs/chapters/06-context-management.md) [09](docs/chapters/09-edge-cloud.md)–[12](docs/chapters/12-agent-security.md) | `examples/09`–`11` + `projects/02` |
| 第 5 周 | VAD、ASR、TTS、对话状态 | [13](docs/chapters/13-voice-agent.md)–[17](docs/chapters/17-tts.md) | `examples/12` |
| 第 6 周 | 企业级语音 Agent 闭环 | [18](docs/chapters/18-projects.md) | `projects/03`–`05` |

## 章节索引

### 第一篇 · Agent 基础与推理

| 章 | 主题 | 文档 |
|----|------|------|
| 1 | 什么是 Agent、核心能力 | [01-agent-basics](docs/chapters/01-agent-basics.md) |
| 2 | ReAct / OODA / Plan&Execute | [02-reasoning-patterns](docs/chapters/02-reasoning-patterns.md) |
| 3 | 主流框架对比与选型 | [03-agent-frameworks](docs/chapters/03-agent-frameworks.md) |

### 第二篇 · 协议、能力与编排

| 章 | 主题 | 文档 |
|----|------|------|
| 4 | MCP 协议 | [04-mcp](docs/chapters/04-mcp.md) |
| 5 | Skill 能力体系 | [05-skill-system](docs/chapters/05-skill-system.md) |
| 6 | 上下文管理 | [06-context-management](docs/chapters/06-context-management.md) |
| 7 | Workflow 编排 | [07-workflow](docs/chapters/07-workflow.md) |
| 8 | Tool Calling | [08-tool-calling](docs/chapters/08-tool-calling.md) |

### 第三篇 · 端云、性能与安全

| 章 | 主题 | 文档 |
|----|------|------|
| 9 | 端云协同 | [09-edge-cloud](docs/chapters/09-edge-cloud.md) |
| 10 | SLM Router | [10-slm-router](docs/chapters/10-slm-router.md) |
| 11 | 缓存策略 | [11-caching](docs/chapters/11-caching.md) |
| 12 | Agent 安全 | [12-agent-security](docs/chapters/12-agent-security.md) |

### 第四篇 · 语音 Agent

| 章 | 主题 | 文档 |
|----|------|------|
| 13 | 语音 Agent 全链路 | [13-voice-agent](docs/chapters/13-voice-agent.md) |
| 14 | VAD | [14-vad](docs/chapters/14-vad.md) |
| 15 | ASR | [15-asr](docs/chapters/15-asr.md) |
| 16 | 对话状态管理 | [16-dialog-state](docs/chapters/16-dialog-state.md) |
| 17 | TTS | [17-tts](docs/chapters/17-tts.md) |
| 18 | 综合项目实践 | [18-projects](docs/chapters/18-projects.md) |

## 可运行示例一览

| 目录 | 对应能力 |
|------|----------|
| [examples/01-weather-agent](examples/01-weather-agent) | Function Calling |
| [examples/02-react-agent](examples/02-react-agent) | ReAct 循环 |
| [examples/03-langgraph-mini](examples/03-langgraph-mini) | Graph / State 状态机思想 |
| [examples/04-mcp-server](examples/04-mcp-server) | 简化版 MCP Server/Client |
| [examples/05-skill-registry](examples/05-skill-registry) | Skill 生命周期 |
| [examples/06-context-memory](examples/06-context-memory) | Sliding Window / Summary Memory |
| [examples/07-workflow](examples/07-workflow) | 线性 Workflow 编排 |
| [examples/08-tool-calling](examples/08-tool-calling) | JSON Schema Tool 闭环 |
| [examples/09-slm-router](examples/09-slm-router) | 端云模型路由 |
| [examples/10-cache](examples/10-cache) | Prompt / Semantic Cache |
| [examples/11-security](examples/11-security) | 注入检测 / 权限 / 审计 |
| [examples/12-voice-pipeline](examples/12-voice-pipeline) | 语音全链路 Mock |

## 综合项目（按难度递进）

| 阶段 | 项目 | 技术点 |
|------|------|--------|
| 入门 | [01-weather](projects/01-weather) | Function / Tool Calling |
| 进阶 | [02-search-agent](projects/02-search-agent) | ReAct、Memory、假搜索/RAG |
| 高级 | [03-multi-agent](projects/03-multi-agent) | 多角色协作 |
| 语音 | [04-voice-assistant](projects/04-voice-assistant) | VAD/ASR/LLM/TTS 状态机 |
| 企业 | [05-enterprise-agent](projects/05-enterprise-agent) | Router、Skill、权限、Workflow |

详细任务书与验收标准见 [第 18 章](docs/chapters/18-projects.md)。

## 核心架构速览

```text
用户 / 麦克风
    │
    ▼
┌─────────┐   ┌─────┐   ┌─────┐
│ VAD/ASR │ → │ LLM │ → │ TTS │   （语音路径，可选）
└─────────┘   └──┬──┘   └─────┘
                 │
        Reason / Plan / Reflect
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
  Memory      Tools/MCP    Workflow
  Session     Skills       Router
  RAG         Sandbox      Cache
```

## 设计说明

- **先原理后框架**：用自实现迷你版本讲清 Graph/ReAct/MCP，再对照 LangGraph、CrewAI 等生产框架。
- **默认可离线运行**：`shared/mock_llm.py` 与语音 Mock 保证无 Key 也能跑通闭环。
- **工程化视角**：覆盖安全、缓存、路由、审计，贴近企业落地，而非仅 Demo Prompt。

## License

MIT
