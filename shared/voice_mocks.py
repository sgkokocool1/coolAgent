"""Text-based voice pipeline mocks for tutorial examples.

The module simulates a voice Agent without microphone, ASR model, LLM service,
or speaker hardware. It keeps the data flow close to a real production stack:
audio events -> VAD endpoint -> ASR transcript -> tool-capable Agent -> TTS.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable


@dataclass(frozen=True)
class AudioEvent:
    """A tiny stand-in for an audio frame emitted by a microphone."""

    kind: str
    text: str = ""
    duration_ms: int = 120
    interrupt: bool = False


@dataclass(frozen=True)
class Utterance:
    """A detected user utterance after VAD endpointing."""

    text: str
    duration_ms: int
    interrupted_previous_tts: bool = False


@dataclass(frozen=True)
class ToolCall:
    """Minimal function-calling record used in the mock Agent."""

    name: str
    arguments: dict[str, str]
    result: str


@dataclass(frozen=True)
class AgentTurn:
    """One complete user-to-assistant turn."""

    user_text: str
    answer: str
    tool_call: ToolCall | None = None


class MockMicrophone:
    """Yields pre-scripted audio events."""

    def __init__(self, events: Iterable[AudioEvent]) -> None:
        self._events = list(events)

    def listen(self) -> Iterable[AudioEvent]:
        for event in self._events:
            print(f"[Mic] {event.kind}: {event.text or '<静音>'}")
            yield event


class MockVAD:
    """Simple start/end detector driven by text events.

    A real VAD receives PCM frames. This mock treats ``speech`` as voiced frames
    and ``silence`` as the endpoint marker after enough speech has accumulated.
    """

    def __init__(self, min_speech_ms: int = 180, endpoint_silence_ms: int = 240) -> None:
        self.min_speech_ms = min_speech_ms
        self.endpoint_silence_ms = endpoint_silence_ms
        self._speech_parts: list[str] = []
        self._speech_ms = 0
        self._silence_ms = 0
        self._interrupted = False

    def accept(self, event: AudioEvent) -> Utterance | None:
        if event.kind == "speech":
            if not self._speech_parts:
                print("[VAD] start_of_speech")
            self._speech_parts.append(event.text)
            self._speech_ms += event.duration_ms
            self._silence_ms = 0
            self._interrupted = self._interrupted or event.interrupt
            return None

        if event.kind == "silence" and self._speech_parts:
            self._silence_ms += event.duration_ms
            if self._speech_ms >= self.min_speech_ms and self._silence_ms >= self.endpoint_silence_ms:
                text = "".join(self._speech_parts).strip()
                utterance = Utterance(text, self._speech_ms, self._interrupted)
                print("[VAD] end_of_speech")
                self.reset()
                return utterance

        return None

    def reset(self) -> None:
        self._speech_parts = []
        self._speech_ms = 0
        self._silence_ms = 0
        self._interrupted = False


class MockASR:
    """Converts a detected utterance into text."""

    def transcribe(self, utterance: Utterance) -> str:
        print(f"[ASR] transcript={utterance.text}")
        return utterance.text


class MockToolRegistry:
    """Small deterministic tool registry for function-calling demos."""

    def __init__(self) -> None:
        self._tools: dict[str, Callable[[dict[str, str]], str]] = {
            "get_weather": self._get_weather,
            "create_reminder": self._create_reminder,
        }

    def run(self, name: str, arguments: dict[str, str]) -> str:
        if name not in self._tools:
            raise KeyError(f"未知工具: {name}")
        return self._tools[name](arguments)

    def _get_weather(self, arguments: dict[str, str]) -> str:
        city = arguments.get("city", "杭州")
        return f"{city} 小雨转多云，22-27 度，东风 2 级。"

    def _create_reminder(self, arguments: dict[str, str]) -> str:
        content = arguments.get("content", "带伞")
        return f"已创建提醒：{content}。"


class MockVoiceAgent:
    """Keyword-based LLM loop that can call tools and then summarize."""

    def __init__(self, tools: MockToolRegistry | None = None) -> None:
        self.tools = tools or MockToolRegistry()
        self.history: list[AgentTurn] = []

    def respond(self, user_text: str) -> AgentTurn:
        tool_call: ToolCall | None = None
        if "天气" in user_text:
            city = "上海" if "上海" in user_text else "杭州"
            arguments = {"city": city}
            result = self.tools.run("get_weather", arguments)
            tool_call = ToolCall("get_weather", arguments, result)
            answer = f"我查到天气了：{result}建议出门带伞。"
        elif "提醒" in user_text or "带伞" in user_text:
            arguments = {"content": "今天出门带伞"}
            result = self.tools.run("create_reminder", arguments)
            tool_call = ToolCall("create_reminder", arguments, result)
            answer = f"{result}我会在出门前再次提示你。"
        else:
            answer = f"我听到了：{user_text}。这是 Mock 语音 Agent 的文本回复。"

        if tool_call:
            print(f"[Tool] {tool_call.name}({tool_call.arguments}) -> {tool_call.result}")
        print(f"[LLM] {answer}")
        turn = AgentTurn(user_text=user_text, answer=answer, tool_call=tool_call)
        self.history.append(turn)
        return turn


class MockTTS:
    """Prints chunks as if audio was streamed to a speaker."""

    def __init__(self, chunk_size: int = 14) -> None:
        self.chunk_size = chunk_size

    def speak(self, text: str, interrupt_after_chunks: int = 0) -> bool:
        chunks = [text[index : index + self.chunk_size] for index in range(0, len(text), self.chunk_size)]
        for index, chunk in enumerate(chunks, start=1):
            print(f"[MockTTS] >>> {chunk}")
            if interrupt_after_chunks and index >= interrupt_after_chunks:
                print("[MockTTS] 用户打断：停止当前播报，等待新的 VAD 端点。")
                return False
        return True


@dataclass
class VoicePipeline:
    """Orchestrates Mic -> VAD -> ASR -> Agent -> TTS."""

    microphone: MockMicrophone
    vad: MockVAD = field(default_factory=MockVAD)
    asr: MockASR = field(default_factory=MockASR)
    agent: MockVoiceAgent = field(default_factory=MockVoiceAgent)
    tts: MockTTS = field(default_factory=MockTTS)

    def run(self) -> list[AgentTurn]:
        turns: list[AgentTurn] = []
        first_answer = True
        for event in self.microphone.listen():
            utterance = self.vad.accept(event)
            if not utterance:
                continue

            if utterance.interrupted_previous_tts:
                print("[Pipeline] 收到用户打断后的新请求。")

            transcript = self.asr.transcribe(utterance)
            turn = self.agent.respond(transcript)
            interrupt_after = 2 if first_answer else 0
            first_answer = False
            self.tts.speak(turn.answer, interrupt_after_chunks=interrupt_after)
            turns.append(turn)

        print("[Pipeline] 流水线结束。")
        return turns


def demo_audio_events() -> list[AudioEvent]:
    """Return a deterministic conversation with one interruption."""

    return [
        AudioEvent("speech", "帮我查一下杭州今天的天气", 260),
        AudioEvent("silence", duration_ms=260),
        AudioEvent("speech", "等等，改成提醒我出门带伞", 260, interrupt=True),
        AudioEvent("silence", duration_ms=260),
    ]
