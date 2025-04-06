import speech_recognition as sr
import pyaudio
import wave
import os
from typing import Optional, Union
import numpy as np

class SpeechController:
    """语音识别控制器，用于处理语音输入和识别"""
    
    def __init__(self):
        """初始化语音识别器"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # 设置音频参数
        self.format = pyaudio.paInt16  # 16位深度
        self.channels = 1  # 单声道
        self.rate = 16000  # 采样率16kHz
        self.chunk = 1024  # 数据块大小
        self.record_seconds = 5  # 默认录音时长
        
        # 调整识别器参数
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def record_audio(self, 
                    output_file: str = "temp.wav",
                    duration: Optional[int] = None) -> str:
        """录制音频
        
        Args:
            output_file: 输出音频文件路径
            duration: 录音时长（秒），如果为None则使用默认时长
            
        Returns:
            str: 录音文件路径
        """
        duration = duration or self.record_seconds
        
        # 初始化PyAudio
        audio = pyaudio.PyAudio()
        
        # 打开音频流
        stream = audio.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        print(f"开始录音，持续{duration}秒...")
        frames = []
        
        # 录制音频
        for i in range(0, int(self.rate / self.chunk * duration)):
            data = stream.read(self.chunk)
            frames.append(data)
        
        print("录音结束")
        
        # 停止并关闭音频流
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # 保存音频文件
        wave_file = wave.open(output_file, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(audio.get_sample_size(self.format))
        wave_file.setframerate(self.rate)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()
        
        return output_file
    
    def recognize_from_microphone(self, 
                                duration: Optional[int] = None,
                                language: str = "zh-CN") -> str:
        """从麦克风录音并识别
        
        Args:
            duration: 录音时长（秒）
            language: 识别语言，默认中文
            
        Returns:
            str: 识别结果文本
        """
        # 录制音频
        audio_file = self.record_audio(duration=duration)
        
        try:
            # 读取音频文件
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            # 识别音频
            text = self.recognizer.recognize_google(audio, language=language)
            print(f"识别结果: {text}")
            
            # 删除临时文件
            if os.path.exists(audio_file):
                os.remove(audio_file)
            
            return text
            
        except sr.UnknownValueError:
            print("无法识别音频内容")
            return ""
        except sr.RequestError as e:
            print(f"请求Google语音识别服务失败: {str(e)}")
            return ""
        finally:
            # 确保临时文件被删除
            if os.path.exists(audio_file):
                os.remove(audio_file)
    
    def recognize_from_file(self, 
                          audio_file: str,
                          language: str = "zh-CN") -> str:
        """从音频文件识别文本
        
        Args:
            audio_file: 音频文件路径
            language: 识别语言，默认中文
            
        Returns:
            str: 识别结果文本
        """
        try:
            # 读取音频文件
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            # 识别音频
            text = self.recognizer.recognize_google(audio, language=language)
            print(f"识别结果: {text}")
            return text
            
        except sr.UnknownValueError:
            print("无法识别音频内容")
            return ""
        except sr.RequestError as e:
            print(f"请求Google语音识别服务失败: {str(e)}")
            return "" 