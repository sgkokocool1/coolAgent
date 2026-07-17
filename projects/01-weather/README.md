# 项目 01：Function Calling 天气 Agent

## 项目目标

实现一个最小 Function Calling Agent：模型根据用户问题生成函数调用，工具返回天气结果，模型再把工具观察组织成最终回答。

## 运行

```bash
python3 projects/01-weather/main.py
```

## 任务说明

1. 阅读 `main.py` 中的 `WeatherAgent.plan()`，理解模型如何把自然语言映射到 `FunctionCall`。
2. 扩展 `WeatherTool.run()` 的假数据，例如加入深圳、成都、广州。
3. 为 `FunctionCall.arguments` 增加日期字段，支持“明天”“周末”等文本。
4. 将 `WeatherTool` 替换成真实天气 API 时，保持 `WeatherAgent.answer()` 的调用接口不变。
5. 增加错误处理：城市未知、工具超时、天气服务返回空结果。

## 验收标准

- 运行脚本后能看到“函数调用”“工具观察”“最终回答”三个阶段。
- 不接入真实网络也能得到稳定输出。
- 新增城市后，用户问题命中该城市时能返回对应天气。
- 工具失败时，Agent 能给出可理解的中文降级回复。
