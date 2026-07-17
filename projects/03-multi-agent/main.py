"""PM/Dev/Tester 多角色协作最小脚手架."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    title: str
    requirement: str


class PMAgent:
    def create_task(self, idea: str) -> Task:
        return Task(
            title="语音备忘录 MVP",
            requirement=f"把想法“{idea}”拆成可演示 MVP：录入文本、保存备忘、列出最近记录。",
        )


class DevAgent:
    def implement_plan(self, task: Task) -> str:
        return (
            f"开发方案：{task.title}\n"
            "1. 使用内存列表保存备忘。\n"
            "2. 暴露 add_note(text) 与 list_notes()。\n"
            "3. CLI 演示固定输入，后续可接入 ASR。"
        )


class TesterAgent:
    def review(self, plan: str) -> str:
        required_checks = ["add_note", "list_notes", "CLI"]
        missing = [check for check in required_checks if check not in plan]
        if missing:
            return f"测试反馈：缺少 {missing}，不能通过。"
        return "测试反馈：通过。验收点覆盖新增备忘、查看备忘和命令行演示。"


class MiniCrew:
    def __init__(self) -> None:
        self.pm = PMAgent()
        self.dev = DevAgent()
        self.tester = TesterAgent()

    def run(self, idea: str) -> str:
        task = self.pm.create_task(idea)
        plan = self.dev.implement_plan(task)
        review = self.tester.review(plan)
        return "\n".join(
            [
                "=== 项目 03：PM/Dev/Tester 多角色协作 ===",
                f"PM 任务：{task.requirement}",
                plan,
                review,
            ]
        )


def main() -> None:
    crew = MiniCrew()
    print(crew.run("做一个可以用语音记录灵感的助手"))


if __name__ == "__main__":
    main()
