"""ReAct + Memory + 假搜索/RAG Agent 最小脚手架."""

from __future__ import annotations

from dataclasses import dataclass, field


DOCUMENTS = {
    "rag": "RAG 通过检索外部知识补充模型上下文，适合知识更新快的业务。",
    "react": "ReAct 把 Thought、Action、Observation 交替组织，让 Agent 可解释地使用工具。",
    "memory": "Memory 可以保存用户偏好、历史问题和中间结论，但需要摘要和过期策略。",
}


@dataclass
class Memory:
    facts: list[str] = field(default_factory=list)

    def remember(self, fact: str) -> None:
        self.facts.append(fact)

    def summary(self) -> str:
        return "；".join(self.facts[-3:]) or "暂无记忆"


class FakeSearch:
    def search(self, query: str) -> list[str]:
        hits = []
        lowered = query.lower()
        for key, value in DOCUMENTS.items():
            if key in lowered or key in query:
                hits.append(value)
        return hits or ["没有命中精确文档，返回默认知识：Agent 需要规划、工具和记忆。"]


class ReActAgent:
    def __init__(self, search: FakeSearch, memory: Memory) -> None:
        self.search = search
        self.memory = memory

    def ask(self, question: str) -> str:
        thought = f"需要先检索资料，再结合记忆回答。当前记忆：{self.memory.summary()}"
        action = f"search({question!r})"
        observations = self.search.search(question)
        joined = " ".join(observations)
        answer = f"根据检索结果：{joined} 我的建议是先用小文档集验证召回质量，再接入真实向量库。"
        self.memory.remember(f"用户关注：{question}")
        return "\n".join(
            [
                f"Thought: {thought}",
                f"Action: {action}",
                f"Observation: {joined}",
                f"Final: {answer}",
            ]
        )


def main() -> None:
    agent = ReActAgent(FakeSearch(), Memory())
    print("=== 项目 02：ReAct + Memory + 假搜索/RAG ===")
    print(agent.ask("RAG 和 ReAct 怎么配合？"))
    print("\n--- 第二轮，展示记忆 ---")
    print(agent.ask("memory 应该保存什么？"))


if __name__ == "__main__":
    main()
