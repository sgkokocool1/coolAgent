from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class WorkflowContext:
    user_request: str
    state: dict[str, Any] = field(default_factory=dict)
    timeline: list[dict[str, Any]] = field(default_factory=list)

    def record(self, step: str, status: str, detail: str, elapsed_ms: float) -> None:
        self.timeline.append(
            {
                "step": step,
                "status": status,
                "detail": detail,
                "elapsed_ms": round(elapsed_ms, 2),
            }
        )


@dataclass(frozen=True)
class Step:
    name: str
    handler: Callable[[WorkflowContext], None]


class WorkflowEngine:
    def __init__(self, steps: list[Step]) -> None:
        self.steps = steps

    def run(self, context: WorkflowContext) -> WorkflowContext:
        for step in self.steps:
            started = time.perf_counter()
            try:
                step.handler(context)
            except Exception as exc:  # pragma: no cover - demo safety net
                elapsed_ms = (time.perf_counter() - started) * 1000
                context.record(step.name, "failed", str(exc), elapsed_ms)
                context.state["error"] = {"step": step.name, "message": str(exc)}
                break
            elapsed_ms = (time.perf_counter() - started) * 1000
            context.record(step.name, "ok", "step completed", elapsed_ms)
        return context


def start_step(context: WorkflowContext) -> None:
    context.state["normalized_request"] = " ".join(context.user_request.strip().split())


def load_profile_tool(context: WorkflowContext) -> None:
    context.state["profile"] = {
        "user_id": "u_demo_001",
        "plan": "team",
        "timezone": "Asia/Shanghai",
        "preferred_language": "zh-CN",
    }


def mock_llm_plan(context: WorkflowContext) -> None:
    if os.getenv("USE_REAL_LLM") == "1":
        context.state["llm_provider"] = "real_api_switch_enabled_but_not_called_in_demo"
    else:
        context.state["llm_provider"] = "mock_rule_engine"

    request = context.state["normalized_request"]
    if "报告" in request:
        action = "generate_report_outline"
    elif "提醒" in request:
        action = "create_reminder"
    else:
        action = "answer_with_context"

    context.state["plan"] = {
        "intent": action,
        "tool_needed": "format_business_response",
        "reason": f"根据用户请求「{request}」选择线性工具处理。",
    }


def format_result_tool(context: WorkflowContext) -> None:
    profile = context.state["profile"]
    plan = context.state["plan"]
    context.state["tool_result"] = {
        "title": "Workflow 执行结果",
        "summary": f"已为 {profile['user_id']} 生成动作 {plan['intent']} 的处理结果。",
        "next_action": "把工具结果交给 End 节点返回给用户。",
    }


def end_step(context: WorkflowContext) -> None:
    result = context.state["tool_result"]
    context.state["final_answer"] = (
        f"{result['title']}：{result['summary']} {result['next_action']}"
    )


def build_workflow() -> WorkflowEngine:
    return WorkflowEngine(
        [
            Step("Start", start_step),
            Step("Tool:LoadProfile", load_profile_tool),
            Step("LLM:Plan", mock_llm_plan),
            Step("Tool:FormatResult", format_result_tool),
            Step("End", end_step),
        ]
    )


def main() -> None:
    context = WorkflowContext(user_request="请帮我生成本周 AI Agent 学习报告")
    result = build_workflow().run(context)

    print("=== 最终回答 ===")
    print(result.state["final_answer"])
    print("\n=== 执行时间线 ===")
    for event in result.timeline:
        print(
            f"{event['step']:<18} {event['status']:<6} "
            f"{event['elapsed_ms']:>6.2f} ms  {event['detail']}"
        )
    print("\n=== 关键状态 ===")
    print(f"LLM provider: {result.state['llm_provider']}")
    print(f"Plan intent : {result.state['plan']['intent']}")


if __name__ == "__main__":
    main()
