import os
from typing import List, Optional, Dict, Any
from groq import Groq
from dotenv import load_dotenv
import base64
from PIL import Image
from io import BytesIO

class GroqController:
    """Groq API控制器，用于处理与Groq API的交互"""
    
    def __init__(self):
        """初始化Groq客户端"""
        # 加载环境变量
        load_dotenv()
        
        # 获取API密钥
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("未找到GROQ_API_KEY环境变量")
        
        # 初始化客户端
        self.client = Groq(api_key=api_key)
        
        # 默认模型
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"  # 使用Llama 4 Scout模型
    
    def _encode_image(self, image: Image.Image) -> str:
        """将PIL图像转换为base64编码
        
        Args:
            image: PIL图像对象
            
        Returns:
            str: base64编码的图像字符串
        """
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    def analyze_image(self, 
                     image: Image.Image,
                     prompt: str = "请详细描述这个图像中的内容。",
                     max_tokens: int = 1000,
                     temperature: float = 0.7) -> str:
        """分析图像内容
        
        Args:
            image: PIL图像对象
            prompt: 提示词
            max_tokens: 最大生成token数
            temperature: 生成温度，控制随机性
            
        Returns:
            str: 分析结果
        """
        # 将图像转换为base64
        base64_image = self._encode_image(image)
        
        try:
            # 创建聊天完成请求
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # 返回生成的文本
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"调用Groq API时发生错误: {str(e)}")
            return f"错误: {str(e)}"
    
    def chat(self, 
            messages: List[Dict[str, str]], 
            max_tokens: int = 1000,
            temperature: float = 0.7) -> str:
        """进行文本聊天
        
        Args:
            messages: 消息列表，每个消息是包含role和content的字典
            max_tokens: 最大生成token数
            temperature: 生成温度，控制随机性
            
        Returns:
            str: 聊天回复
        """
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"调用Groq API时发生错误: {str(e)}")
            return f"错误: {str(e)}" 