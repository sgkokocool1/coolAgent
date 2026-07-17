"""Function Calling 天气 Agent 最小脚手架."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FunctionCall:
    name: str
    arguments: dict[str, str]


class WeatherTool:
    def run(self, city: str) -> str:
        fake_weather = {
            "北京": "晴，18-29 度，空气质量良。",
            "上海": "多云转小雨，23-28 度，湿度较高。",
            "杭州": "小雨，22-27 度，建议带伞。",
        }
        return fake_weather.get(city, f"{city} 晴到多云，20-28 度。")


class WeatherAgent:
    def __init__(self, weather_tool: WeatherTool) -> None:
        self.weather_tool = weather_tool

    def plan(self, user_text: str) -> FunctionCall | None:
        if "天气" not in user_text:
            return None
        for city in ["北京", "上海", "杭州"]:
            if city in user_text:
                return FunctionCall("get_weather", {"city": city})
        return FunctionCall("get_weather", {"city": "杭州"})

    def answer(self, user_text: str) -> str:
        call = self.plan(user_text)
        if call is None:
            return "我目前只演示天气查询能力，请问你想查哪个城市？"

        city = call.arguments["city"]
        observation = self.weather_tool.run(city)
        return (
            f"函数调用：{call.name}({call.arguments})\n"
            f"工具观察：{observation}\n"
            f"最终回答：{city}今天{observation}如果外出，请根据降雨情况准备雨具。"
        )


def main() -> None:
    agent = WeatherAgent(WeatherTool())
    question = "帮我查一下杭州今天的天气"
    print("=== 项目 01：Function Calling 天气 Agent ===")
    print(f"用户：{question}")
    print(agent.answer(question))


if __name__ == "__main__":
    main()
