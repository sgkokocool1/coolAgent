from __future__ import annotations

import os
from dataclasses import dataclass


PRIVACY_KEYWORDS = {"身份证", "银行卡", "住址", "手机号", "密码", "token", "api key"}
COMPLEX_KEYWORDS = {"分析", "规划", "比较", "总结", "设计", "推理", "架构", "多步骤"}


@dataclass(frozen=True)
class Request:
    text: str
    latency_budget_ms: int
    max_cost_usd: float


@dataclass(frozen=True)
class RouteDecision:
    model_name: str
    privacy_level: str
    complexity: int
    estimated_cost_usd: float
    reasons: list[str]


def estimate_privacy(text: str) -> str:
    lowered = text.lower()
    if any(keyword.lower() in lowered for keyword in PRIVACY_KEYWORDS):
        return "high"
    return "normal"


def estimate_complexity(text: str) -> int:
    score = 1
    score += min(len(text) // 20, 4)
    score += sum(2 for keyword in COMPLEX_KEYWORDS if keyword in text)
    if "？" in text or "?" in text:
        score += 1
    return min(score, 10)


def route_request(request: Request) -> RouteDecision:
    privacy = estimate_privacy(request.text)
    complexity = estimate_complexity(request.text)
    reasons: list[str] = []

    if privacy == "high":
        reasons.append("检测到高隐私关键词，优先端侧处理")
        return RouteDecision("mock_local_slm", privacy, complexity, 0.0, reasons)

    if request.latency_budget_ms < 500:
        reasons.append("延迟预算低于 500ms，选择本地 SLM")
        return RouteDecision("mock_local_slm", privacy, complexity, 0.0, reasons)

    if complexity >= 8:
        estimated_cost = 0.08
        if request.max_cost_usd >= estimated_cost:
            reasons.append("复杂度较高且预算允许，选择强云模型")
            return RouteDecision("mock_claude", privacy, complexity, estimated_cost, reasons)
        reasons.append("复杂度较高但预算不足，降级到便宜云模型")
        return RouteDecision("mock_cloud_gpt", privacy, complexity, 0.02, reasons)

    if request.max_cost_usd < 0.01:
        reasons.append("成本预算很低，选择本地 SLM")
        return RouteDecision("mock_local_slm", privacy, complexity, 0.0, reasons)

    reasons.append("普通复杂度请求，选择便宜云模型")
    return RouteDecision("mock_cloud_gpt", privacy, complexity, 0.02, reasons)


def mock_local_slm(prompt: str) -> str:
    return f"[local_slm] 已在端侧处理：{prompt[:24]}..."


def mock_cloud_gpt(prompt: str) -> str:
    if os.getenv("USE_REAL_CLOUD_MODEL") == "1":
        return "[cloud_gpt] 真实 API 开关已启用；示例仍返回 Mock 结果。"
    return f"[cloud_gpt] 使用低成本云模型回答：{prompt}"


def mock_claude(prompt: str) -> str:
    if os.getenv("USE_REAL_CLOUD_MODEL") == "1":
        return "[claude] 真实 API 开关已启用；示例仍返回 Mock 结果。"
    return f"[claude] 使用强推理模型生成分层分析：{prompt}"


def execute_model(decision: RouteDecision, prompt: str) -> str:
    models = {
        "mock_local_slm": mock_local_slm,
        "mock_cloud_gpt": mock_cloud_gpt,
        "mock_claude": mock_claude,
    }
    return models[decision.model_name](prompt)


def main() -> None:
    requests = [
        Request("打开客厅灯", latency_budget_ms=200, max_cost_usd=0.001),
        Request("请比较 LangGraph 和 Temporal 在企业 Agent 编排中的差异", 2500, 0.05),
        Request("我的身份证是 110101199001010000，请帮我记住", 1000, 0.10),
        Request("请设计一个多步骤语音 Agent 架构并分析成本、隐私和延迟", 3000, 0.10),
    ]

    for item in requests:
        decision = route_request(item)
        answer = execute_model(decision, item.text)
        print("\n=== 请求 ===")
        print(item.text)
        print("路由结果：")
        print(f"- model            : {decision.model_name}")
        print(f"- privacy_level    : {decision.privacy_level}")
        print(f"- complexity       : {decision.complexity}")
        print(f"- estimated_cost   : ${decision.estimated_cost_usd:.2f}")
        print(f"- reasons          : {'；'.join(decision.reasons)}")
        print("模型输出：")
        print(answer)


if __name__ == "__main__":
    main()
