# 项目 05：企业端 Agent 骨架

## 项目目标

搭建一个企业端 Agent 的最小骨架，覆盖 SLM Router、Skill Registry、Permission Guard 和 Workflow Engine。

## 运行

```bash
python3 projects/05-enterprise-agent/main.py
```

## 模块说明

- **SLMRouter**：根据意图选择小模型、RAG 模型或强推理模型。
- **SkillRegistry**：注册企业技能，例如制度查询、审批流、合同生成。
- **PermissionGuard**：在执行高风险动作前检查用户角色。
- **WorkflowEngine**：串联路由、权限、技能和最终回复。

## 任务说明

1. 给 `SLMRouter.route()` 增加成本与延迟策略，例如普通问答优先小模型。
2. 将 `SkillRegistry` 改成字典注册模式，支持动态新增技能。
3. 扩展 `PermissionGuard`，加入部门、数据范围和审批金额限制。
4. 给 `WorkflowEngine.handle()` 增加审计日志，记录谁在什么时候调用了什么技能。
5. 把固定用户替换成来自 SSO/JWT 的身份信息。

## 验收标准

- 运行脚本能看到模型路由、技能结果和权限拒绝示例。
- 普通员工不能发起需要经理权限的审批。
- 经理角色可以通过同一工作流发起审批。
- 新增技能不需要改动权限检查代码。
