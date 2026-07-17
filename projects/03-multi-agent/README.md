# 项目 03：PM/Dev/Tester 多角色协作

## 项目目标

自实现一个轻量 crew 风格协作框架，让 PM、Dev、Tester 三个角色围绕同一任务传递结构化结果。

## 运行

```bash
python3 projects/03-multi-agent/main.py
```

## 任务说明

1. `PMAgent` 负责把用户想法整理成 `Task`。
2. `DevAgent` 负责把任务转成可执行技术方案。
3. `TesterAgent` 负责检查方案是否覆盖验收点。
4. `MiniCrew` 负责调度角色顺序和汇总结果。
5. 后续可以加入 Reviewer、Security、Ops 等角色，但要保持每个角色输入输出清晰。

## 扩展练习

- 给 `Task` 增加优先级、风险和截止时间。
- 让 `TesterAgent` 返回多条缺陷，而不是单个字符串。
- 支持角色重试：测试不通过时把反馈交回 Dev 修改方案。
- 把角色回复保存为 JSON，方便前端或工作流系统展示。

## 验收标准

- 运行脚本后能看到 PM、Dev、Tester 三段输出。
- Tester 能根据计划内容判断通过或不通过。
- 新增角色时无需修改已有角色类的内部实现。
