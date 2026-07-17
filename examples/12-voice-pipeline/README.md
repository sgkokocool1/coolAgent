# 示例 12：Mock 语音流水线

本示例用文本模拟完整语音 Agent，不依赖麦克风、ASR 模型、LLM API 或声卡。

## 运行

```bash
python3 examples/12-voice-pipeline/main.py
```

## 链路

1. **Mic**：`MockMicrophone` 读取预设的假音频事件。
2. **VAD**：`MockVAD` 根据 `speech`/`silence` 判断起点和端点。
3. **ASR**：`MockASR` 把检测到的语音片段转成文本。
4. **LLM**：`MockVoiceAgent` 根据文本决定是否调用工具。
5. **Tool**：天气和提醒工具返回确定性结果。
6. **LLM**：Agent 汇总工具结果形成自然语言回复。
7. **TTS**：`MockTTS` 分块打印拟语音。
8. **Speaker**：终端输出代表扬声器播放。

## 打断模拟

第一轮 TTS 播报到一半时会打印“用户打断”，随后第二段假音频进入 VAD，并触发新的 ASR 与 Agent 回合。这个流程对应真实系统中的 barge-in：检测到用户新语音后停止当前播报，清空或更新播放队列，再处理新的用户意图。
