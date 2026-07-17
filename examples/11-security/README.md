# 示例 11：Agent 安全防线

本示例演示四类基础安全控制：

- Prompt Injection 检测。
- Tool 权限白名单。
- 输出敏感信息过滤。
- 审计日志。

运行：

```bash
python main.py
```

示例中包含四个请求：

1. guest 查询 FAQ，允许执行。
2. guest 创建工单，被权限系统拒绝。
3. admin 查看内部状态，输出中的 token 会被过滤。
4. employee 发起 Prompt Injection，被输入检测拒绝。

真实系统中应把关键词检测升级为策略引擎或安全分类模型，并把审计日志写入不可篡改的日志系统。
