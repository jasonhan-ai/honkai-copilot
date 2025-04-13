import pyttsx3
import threading
from typing import Optional

class TTSController:
    def __init__(self):
        """初始化TTS控制器"""
        self.rate = 150  # 默认语速
        self.volume = 0.9  # 默认音量
        self.voice_id = None  # 默认语音ID
        self._init_voice()
    
    def _init_voice(self):
        """初始化语音设置"""
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'chinese' in voice.name.lower() or 'zh' in voice.id.lower():
                self.voice_id = voice.id
                break
    
    def _create_engine(self):
        """创建新的引擎实例"""
        engine = pyttsx3.init()
        engine.setProperty('rate', self.rate)
        engine.setProperty('volume', self.volume)
        if self.voice_id:
            engine.setProperty('voice', self.voice_id)
        return engine
    
    def speak(self, text: str, block: bool = False) -> None:
        """
        将文本转换为语音并播放
        
        Args:
            text: 要转换为语音的文本
            block: 是否阻塞等待语音播放完成
        """
        if block:
            engine = self._create_engine()
            engine.say(text)
            engine.runAndWait()
        else:
            # 在新线程中播放语音，避免阻塞主线程
            thread = threading.Thread(target=self._speak_in_thread, args=(text,))
            thread.daemon = True
            thread.start()
    
    def _speak_in_thread(self, text: str) -> None:
        """在新线程中播放语音"""
        engine = self._create_engine()
        engine.say(text)
        engine.runAndWait()
    
    def stop(self) -> None:
        """停止当前正在播放的语音"""
        # 由于每次都是新的引擎实例，这个方法实际上不需要做任何事情
        pass
    
    def set_rate(self, rate: int) -> None:
        """
        设置语速
        
        Args:
            rate: 语速，范围通常在50-400之间
        """
        self.rate = rate
    
    def set_volume(self, volume: float) -> None:
        """
        设置音量
        
        Args:
            volume: 音量，范围在0.0-1.0之间
        """
        self.volume = volume
    
    def get_available_voices(self) -> list:
        """获取可用的语音列表"""
        engine = self._create_engine()
        return engine.getProperty('voices')
    
    def set_voice(self, voice_id: str) -> None:
        """
        设置语音
        
        Args:
            voice_id: 语音ID
        """
        self.voice_id = voice_id 