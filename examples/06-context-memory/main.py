from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Message:
    role: str
    content: str


@dataclass
class SlidingSummaryMemory:
    window_size: int = 3
    summary: str = ""
    window: list[Message] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.window.append(Message(role=role, content=content))
        self.compact_if_needed()

    def compact_if_needed(self) -> None:
        while len(self.window) > self.window_size:
            oldest = self.window.pop(0)
            self.summary = self.merge_summary(self.summary, oldest)

    def merge_summary(self, current_summary: str, message: Message) -> str:
        fact = f"{message.role}: {message.content}"
        if not current_summary:
            return fact
        return f"{current_summary} | {fact}"

    def build_context(self) -> list[dict[str, str]]:
        context: list[dict[str, str]] = []
        if self.summary:
            context.append({"role": "system", "content": f"历史摘要：{self.summary}"})
        context.extend({"role": message.role, "content": message.content} for message in self.window)
        return context


def print_memory(memory: SlidingSummaryMemory, turn: int) -> None:
    print(f"第 {turn} 轮后")
    print("Summary:", memory.summary or "空")
    print("Window:")
    for message in memory.window:
        print(f"  - {message.role}: {message.content}")
    print("Context:")
    for item in memory.build_context():
        print(f"  - {item['role']}: {item['content']}")
    print("-" * 60)


def main() -> None:
    memory = SlidingSummaryMemory(window_size=3)
    conversation = [
        ("user", "我想学习 AI Agent，要求全部用中文。"),
        ("assistant", "好的，我们先从 Agent 基础概念开始。"),
        ("user", "请记住我偏好可运行的 Python 示例。"),
        ("assistant", "我会优先提供 Python 3.11+ 示例。"),
        ("user", "接下来讲 ReAct，并关联天气工具。"),
        ("assistant", "ReAct 可以通过 Thought、Action、Observation 循环调用天气工具。"),
    ]

    for index, (role, content) in enumerate(conversation, start=1):
        memory.add_message(role, content)
        print_memory(memory, index)

    print("最终给 LLM 的上下文只包含摘要和最近窗口，避免历史无限增长。")


if __name__ == "__main__":
    main()
