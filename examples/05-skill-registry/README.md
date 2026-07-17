# 示例 05：Skill 注册、发现、调用与日志生命周期

## 目标

演示一个最小 Skill System：把任务能力注册到 `SkillRegistry`，根据用户任务关键词发现匹配 Skill，依次调用处理函数，并记录生命周期日志。

## 运行方式

```bash
python main.py
```

如果本机没有 `python` 命令，请使用 `python3 main.py`。

## 核心代码说明

- `Skill` 描述技能名称、说明、触发关键词和处理函数。
- `SkillRegistry.register()` 把 Skill 加入注册表，并记录 `registered` 事件。
- `SkillRegistry.discover()` 根据关键词发现候选 Skill，并记录 `discovered` 事件。
- `SkillRegistry.invoke()` 调用 Skill handler，并记录 `invoked` 与 `completed` 事件。
- 示例注册了天气、计算和总结三个 Skill，展示一个任务如何触发多个能力。
