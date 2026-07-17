"""Mock voice Agent pipeline demo.

Run:
    python3 examples/12-voice-pipeline/main.py
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.voice_mocks import MockMicrophone, VoicePipeline, demo_audio_events


def main() -> None:
    print("=== Mock 语音 Agent 流水线 ===")
    print("链路：Mic -> VAD -> ASR -> LLM -> Tool -> LLM -> TTS -> Speaker")
    microphone = MockMicrophone(demo_audio_events())
    pipeline = VoicePipeline(microphone=microphone)
    turns = pipeline.run()

    print("\n=== 对话摘要 ===")
    for index, turn in enumerate(turns, start=1):
        tool = f"，工具={turn.tool_call.name}" if turn.tool_call else ""
        print(f"{index}. 用户：{turn.user_text} -> 助手：{turn.answer}{tool}")


if __name__ == "__main__":
    main()
