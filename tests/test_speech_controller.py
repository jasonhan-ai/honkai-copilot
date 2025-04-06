import pytest
from src.speech_controller import SpeechController
import os

def test_record_audio():
    """测试音频录制功能"""
    controller = SpeechController()
    
    # 测试3秒录音
    print("\n准备录制3秒音频...")
    output_file = "test_record.wav"
    recorded_file = controller.record_audio(
        output_file=output_file,
        duration=3
    )
    
    # 验证文件是否创建
    assert os.path.exists(recorded_file)
    assert os.path.getsize(recorded_file) > 0
    
    # 清理测试文件
    os.remove(recorded_file)

def test_speech_recognition():
    """测试语音识别功能"""
    controller = SpeechController()
    
    print("\n请在接下来的3秒内说一些话...")
    text = controller.recognize_from_microphone(duration=3)
    
    # 验证返回结果
    assert isinstance(text, str)
    print(f"识别结果: {text}")

if __name__ == "__main__":
    # 运行单个测试
    test_speech_recognition() 