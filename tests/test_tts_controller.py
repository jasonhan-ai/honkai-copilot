import unittest
from src.tts_controller import TTSController

class TestTTSController(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.tts = TTSController()
    
    def test_speak(self):
        """测试语音播放功能"""
        # 测试阻塞模式
        self.tts.speak("这是一条测试语音", block=True)
        
        # 测试非阻塞模式
        self.tts.speak("这是另一条测试语音", block=False)
    
    def test_voice_settings(self):
        """测试语音设置"""
        # 测试语速设置
        self.tts.set_rate(200)
        self.tts.speak("语速测试", block=True)
        
        # 测试音量设置
        self.tts.set_volume(0.5)
        self.tts.speak("音量测试", block=True)
    
    def test_available_voices(self):
        """测试获取可用语音列表"""
        voices = self.tts.get_available_voices()
        self.assertIsInstance(voices, list)
        print("可用的语音列表：")
        for voice in voices:
            print(f"ID: {voice.id}, Name: {voice.name}")

if __name__ == '__main__':
    unittest.main() 