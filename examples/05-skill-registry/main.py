from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable


SkillHandler = Callable[[str], str]


@dataclass
class Skill:
    name: str
    description: str
    keywords: list[str]
    handler: SkillHandler


@dataclass
class SkillEvent:
    skill_name: str
    stage: str
    detail: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))


class SkillRegistry:
    def __init__(self) -> None:
        self.skills: dict[str, Skill] = {}
        self.events: list[SkillEvent] = []

    def register(self, skill: Skill) -> None:
        self.skills[skill.name] = skill
        self.log(skill.name, "registered", skill.description)

    def discover(self, task: str) -> list[Skill]:
        matched: list[Skill] = []
        for skill in self.skills.values():
            if any(keyword in task for keyword in skill.keywords):
                matched.append(skill)
                self.log(skill.name, "discovered", f"任务匹配关键词: {task}")
        return matched

    def invoke(self, skill: Skill, task: str) -> str:
        self.log(skill.name, "invoked", "开始执行 Skill")
        result = skill.handler(task)
        self.log(skill.name, "completed", result)
        return result

    def log(self, skill_name: str, stage: str, detail: str) -> None:
        self.events.append(SkillEvent(skill_name=skill_name, stage=stage, detail=detail))


def weather_skill(task: str) -> str:
    city = "北京" if "北京" in task else "杭州"
    weather = {"北京": "晴，28℃", "杭州": "小雨，26℃"}[city]
    return f"天气 Skill：{city}当前{weather}。"


def calculator_skill(task: str) -> str:
    return "计算 Skill：3 * 7 = 21。"


def summary_skill(task: str) -> str:
    return f"总结 Skill：任务包含 {len(task)} 个字符，核心意图是获取结构化结果。"


def build_registry() -> SkillRegistry:
    registry = SkillRegistry()
    registry.register(
        Skill(
            name="weather-advisor",
            description="查询模拟天气并给出建议",
            keywords=["天气", "温度", "下雨"],
            handler=weather_skill,
        )
    )
    registry.register(
        Skill(
            name="calculator",
            description="执行简单算术说明",
            keywords=["计算", "*", "+", "-", "/"],
            handler=calculator_skill,
        )
    )
    registry.register(
        Skill(
            name="summarizer",
            description="总结用户任务",
            keywords=["总结", "概括", "说明"],
            handler=summary_skill,
        )
    )
    return registry


def main() -> None:
    task = "请查询北京天气，计算 3 * 7，并总结一下结果。"
    registry = build_registry()
    print("任务：", task)
    print("=" * 60)

    matched_skills = registry.discover(task)
    for skill in matched_skills:
        print(registry.invoke(skill, task))

    print("=" * 60)
    print("生命周期日志：")
    for event in registry.events:
        print(f"[{event.timestamp}] {event.skill_name} -> {event.stage}: {event.detail}")


if __name__ == "__main__":
    main()
