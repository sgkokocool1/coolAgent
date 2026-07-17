from __future__ import annotations

import ast
import operator
from dataclasses import dataclass, field
from typing import Any, Callable


WEATHER_DATA = {
    "北京": "晴，28℃，东北风 2 级",
    "上海": "多云，30℃，东南风 3 级",
    "杭州": "小雨，26℃，北风 2 级",
}


def get_weather(city: str) -> str:
    return WEATHER_DATA.get(city, "没有该城市的模拟天气数据")


ALLOWED_OPERATORS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def calculator(expression: str) -> str:
    node = ast.parse(expression, mode="eval")

    def eval_node(current: ast.AST) -> float:
        if isinstance(current, ast.Expression):
            return eval_node(current.body)
        if isinstance(current, ast.Constant) and isinstance(current.value, (int, float)):
            return float(current.value)
        if isinstance(current, ast.BinOp) and type(current.op) in ALLOWED_OPERATORS:
            left = eval_node(current.left)
            right = eval_node(current.right)
            return ALLOWED_OPERATORS[type(current.op)](left, right)
        raise ValueError(f"不支持的表达式: {expression}")

    result = eval_node(node)
    return str(int(result)) if result.is_integer() else str(result)


@dataclass
class ReActState:
    question: str
    observations: list[str] = field(default_factory=list)
    weather_done: bool = False
    calculation_done: bool = False


class ReActAgent:
    def __init__(self) -> None:
        self.tools: dict[str, Callable[..., str]] = {
            "get_weather": get_weather,
            "calculator": calculator,
        }

    def run(self, question: str) -> str:
        state = ReActState(question=question)

        for step_index in range(1, 6):
            thought, action = self.plan_next_step(state)
            print(f"Thought {step_index}: {thought}")

            if action is None:
                answer = self.final_answer(state)
                print(f"Final Answer: {answer}")
                return answer

            tool_name, arguments = action
            print(f"Action {step_index}: {tool_name}({arguments})")
            observation = self.invoke_tool(tool_name, arguments)
            print(f"Observation {step_index}: {observation}")
            print("-" * 60)
            state.observations.append(f"{tool_name}: {observation}")

            if tool_name == "get_weather":
                state.weather_done = True
            if tool_name == "calculator":
                state.calculation_done = True

        raise RuntimeError("ReAct 循环超过最大步数")

    def plan_next_step(self, state: ReActState) -> tuple[str, tuple[str, dict[str, Any]] | None]:
        if not state.weather_done and "天气" in state.question:
            return "问题询问天气，我需要先获取城市天气。", ("get_weather", {"city": "北京"})

        if not state.calculation_done and any(symbol in state.question for symbol in ["计算", "*", "+", "-", "/"]):
            return "问题还要求计算数值，我需要调用安全计算器。", ("calculator", {"expression": "3 * 7"})

        return "已经获得天气和计算结果，可以生成最终回答。", None

    def invoke_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        tool = self.tools[tool_name]
        return tool(**arguments)

    def final_answer(self, state: ReActState) -> str:
        joined = "；".join(state.observations)
        return f"根据工具观察：{joined}。北京适合短时间户外活动，3 * 7 = 21。"


def main() -> None:
    question = "请查询北京天气，并计算 3 * 7，然后给我一个简短建议。"
    print("用户：", question)
    print("=" * 60)
    ReActAgent().run(question)


if __name__ == "__main__":
    main()
