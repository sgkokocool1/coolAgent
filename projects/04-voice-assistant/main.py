"""语音助手状态机脚手架."""

from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.voice_mocks import MockMicrophone, VoicePipeline, demo_audio_events


class VoiceState(str, Enum):
    IDLE = "空闲"
    LISTENING = "聆听"
    THINKING = "思考"
    SPEAKING = "播报"
    INTERRUPTED = "被打断"


class VoiceAssistantStateMachine:
    def __init__(self) -> None:
        self.state = VoiceState.IDLE

    def transition(self, next_state: VoiceState, reason: str) -> None:
        print(f"[State] {self.state.value} -> {next_state.value}：{reason}")
        self.state = next_state

    def run_demo(self) -> None:
        self.transition(VoiceState.LISTENING, "检测到唤醒词")
        pipeline = VoicePipeline(MockMicrophone(demo_audio_events()))
        turns = pipeline.run()
        self.transition(VoiceState.INTERRUPTED, "第一轮播报期间用户插话")
        self.transition(VoiceState.THINKING, "处理新的用户意图")
        self.transition(VoiceState.SPEAKING, "播放最新回复")
        self.transition(VoiceState.IDLE, f"完成 {len(turns)} 轮对话")


def main() -> None:
    print("=== 项目 04：语音助手状态机脚手架 ===")
    assistant = VoiceAssistantStateMachine()
    assistant.run_demo()


if __name__ == "__main__":
    main()
