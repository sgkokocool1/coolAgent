from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


State = dict[str, object]
Node = Callable[[State], State]
Condition = Callable[[State], bool]


@dataclass
class Edge:
    target: str
    condition: Condition | None = None


@dataclass
class MiniGraph:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: dict[str, list[Edge]] = field(default_factory=dict)
    entrypoint: str | None = None
    finish_nodes: set[str] = field(default_factory=set)

    def add_node(self, name: str, node: Node) -> None:
        self.nodes[name] = node

    def add_edge(self, source: str, target: str, condition: Condition | None = None) -> None:
        self.edges.setdefault(source, []).append(Edge(target=target, condition=condition))

    def set_entrypoint(self, name: str) -> None:
        self.entrypoint = name

    def add_finish_node(self, name: str) -> None:
        self.finish_nodes.add(name)

    def run(self, initial_state: State) -> State:
        if self.entrypoint is None:
            raise ValueError("缺少 entrypoint")

        current = self.entrypoint
        state = dict(initial_state)
        visited_steps = 0

        while True:
            visited_steps += 1
            if visited_steps > 20:
                raise RuntimeError("图执行超过最大步数")

            print(f"Node: {current}")
            state = self.nodes[current](state)
            print(f"State: {state}")
            print("-" * 60)

            if current in self.finish_nodes:
                return state

            current = self.next_node(current, state)

    def next_node(self, current: str, state: State) -> str:
        for edge in self.edges.get(current, []):
            if edge.condition is None or edge.condition(state):
                return edge.target
        raise RuntimeError(f"节点 {current} 没有可用出边")


def parse_intent(state: State) -> State:
    question = str(state["question"])
    state["need_weather"] = "天气" in question
    state["city"] = "北京" if "北京" in question else "杭州"
    return state


def call_weather_tool(state: State) -> State:
    city = str(state["city"])
    weather = {
        "北京": "晴，28℃，空气质量良好",
        "杭州": "小雨，26℃，建议带伞",
    }.get(city, "没有模拟数据")
    state["weather"] = weather
    return state


def generate_answer(state: State) -> State:
    if state.get("need_weather"):
        state["answer"] = f"{state['city']}天气：{state['weather']}。这是由图状态机 Agent 生成的回复。"
    else:
        state["answer"] = "这个问题不需要天气工具，直接回复即可。"
    return state


def build_graph() -> MiniGraph:
    graph = MiniGraph()
    graph.add_node("parse_intent", parse_intent)
    graph.add_node("call_weather_tool", call_weather_tool)
    graph.add_node("generate_answer", generate_answer)

    graph.set_entrypoint("parse_intent")
    graph.add_edge("parse_intent", "call_weather_tool", lambda state: bool(state.get("need_weather")))
    graph.add_edge("parse_intent", "generate_answer", lambda state: not bool(state.get("need_weather")))
    graph.add_edge("call_weather_tool", "generate_answer")
    graph.add_finish_node("generate_answer")
    return graph


def main() -> None:
    graph = build_graph()
    final_state = graph.run({"question": "北京天气如何？"})
    print("Final:", final_state["answer"])


if __name__ == "__main__":
    main()
