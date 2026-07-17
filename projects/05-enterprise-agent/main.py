"""企业端 Agent：SLM Router + Skill + 权限 + Workflow 骨架."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    name: str
    roles: set[str]


@dataclass(frozen=True)
class Request:
    user: User
    intent: str
    payload: dict[str, str]


class PermissionGuard:
    def assert_allowed(self, request: Request, required_role: str) -> None:
        if required_role not in request.user.roles:
            raise PermissionError(f"{request.user.name} 缺少权限：{required_role}")


class SLMRouter:
    def route(self, request: Request) -> str:
        if request.intent in {"查制度", "查知识库"}:
            return "small-rag-model"
        if request.intent in {"审批", "生成合同"}:
            return "large-reasoning-model"
        return "small-chat-model"


class SkillRegistry:
    def run(self, skill_name: str, payload: dict[str, str]) -> str:
        if skill_name == "policy_search":
            keyword = payload.get("keyword", "报销")
            return f"知识库命中：{keyword} 需要直属主管审批，金额超过 5000 元需财务复核。"
        if skill_name == "approval_workflow":
            item = payload.get("item", "采购申请")
            return f"已创建审批流：{item} -> 主管 -> 财务 -> 归档。"
        return "技能未注册。"


class WorkflowEngine:
    def __init__(self, guard: PermissionGuard, router: SLMRouter, skills: SkillRegistry) -> None:
        self.guard = guard
        self.router = router
        self.skills = skills

    def handle(self, request: Request) -> str:
        model = self.router.route(request)
        if request.intent == "查制度":
            observation = self.skills.run("policy_search", request.payload)
            return f"模型路由：{model}\n技能结果：{observation}\n回复：请按制度提交材料。"

        if request.intent == "审批":
            self.guard.assert_allowed(request, "manager")
            observation = self.skills.run("approval_workflow", request.payload)
            return f"模型路由：{model}\n技能结果：{observation}\n回复：审批流已启动。"

        return f"模型路由：{model}\n回复：已记录请求，等待人工配置技能。"


def main() -> None:
    print("=== 项目 05：企业端 Agent 骨架 ===")
    engine = WorkflowEngine(PermissionGuard(), SLMRouter(), SkillRegistry())
    employee = User("小李", {"employee"})
    manager = User("王经理", {"employee", "manager"})

    print(engine.handle(Request(employee, "查制度", {"keyword": "差旅报销"})))
    print("\n--- 权限控制示例 ---")
    try:
        print(engine.handle(Request(employee, "审批", {"item": "电脑采购"})))
    except PermissionError as exc:
        print(f"拒绝：{exc}")
    print("\n--- 经理审批示例 ---")
    print(engine.handle(Request(manager, "审批", {"item": "电脑采购"})))


if __name__ == "__main__":
    main()
