from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass
class CacheEntry:
    prompt: str
    answer: str
    cost_usd: float


class PromptCache:
    def __init__(self) -> None:
        self._items: dict[str, CacheEntry] = {}

    @staticmethod
    def normalize(prompt: str) -> str:
        return " ".join(prompt.lower().strip().split())

    def make_key(self, prompt: str, model: str) -> str:
        raw = f"{model}:{self.normalize(prompt)}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, prompt: str, model: str) -> CacheEntry | None:
        return self._items.get(self.make_key(prompt, model))

    def set(self, prompt: str, model: str, answer: str, cost_usd: float) -> None:
        self._items[self.make_key(prompt, model)] = CacheEntry(prompt, answer, cost_usd)


class SemanticCache:
    def __init__(self, threshold: float = 0.72) -> None:
        self.threshold = threshold
        self._items: list[CacheEntry] = []

    def get(self, prompt: str) -> tuple[CacheEntry, float] | None:
        best: tuple[CacheEntry, float] | None = None
        for entry in self._items:
            score = SequenceMatcher(None, normalize_text(prompt), normalize_text(entry.prompt)).ratio()
            if score >= self.threshold and (best is None or score > best[1]):
                best = (entry, score)
        return best

    def set(self, prompt: str, answer: str, cost_usd: float) -> None:
        self._items.append(CacheEntry(prompt, answer, cost_usd))


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def mock_llm(prompt: str) -> tuple[str, float]:
    if os.getenv("USE_REAL_LLM") == "1":
        return "真实 LLM 开关已启用；本地示例仍使用 Mock 成本。", 0.03
    estimated_tokens = max(len(prompt) // 2, 8)
    cost = estimated_tokens * 0.0002
    return f"Mock LLM 回答：已处理「{prompt}」。", round(cost, 4)


def answer_with_cache(
    prompt: str,
    model: str,
    prompt_cache: PromptCache,
    semantic_cache: SemanticCache,
) -> tuple[str, str, float, float | None]:
    exact = prompt_cache.get(prompt, model)
    if exact:
        return exact.answer, "prompt_cache", exact.cost_usd, None

    semantic = semantic_cache.get(prompt)
    if semantic:
        entry, score = semantic
        return entry.answer + "（来自语义相似缓存）", "semantic_cache", entry.cost_usd, score

    answer, cost = mock_llm(prompt)
    prompt_cache.set(prompt, model, answer, cost)
    semantic_cache.set(prompt, answer, cost)
    return answer, "miss_llm", cost, None


def main() -> None:
    model = "mock-gpt-lite-v1"
    prompt_cache = PromptCache()
    semantic_cache = SemanticCache(threshold=0.62)
    total_saved = 0.0

    prompts = [
        "请解释什么是 AI Agent Workflow",
        "请解释什么是 AI Agent Workflow",
        "帮我解释一下 AI Agent 的 Workflow 是什么",
        "Redis 缓存在 Agent 系统里有什么用",
    ]

    for prompt in prompts:
        answer, source, original_cost, similarity = answer_with_cache(
            prompt, model, prompt_cache, semantic_cache
        )
        saved = original_cost if source != "miss_llm" else 0.0
        total_saved += saved

        print("\n=== 请求 ===")
        print(prompt)
        print(f"命中类型：{source}")
        if similarity is not None:
            print(f"语义相似度：{similarity:.2f}")
        print(f"本次节省：${saved:.4f}")
        print(answer)

    print("\n=== 汇总 ===")
    print(f"累计节省 Mock 成本：${total_saved:.4f}")
    print("如需接入 Redis，可把 PromptCache 的 dict 替换为 Redis GET/SET。")


if __name__ == "__main__":
    main()
