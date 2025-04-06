import pytest
from src.groq_controller import GroqController
from src.input_controller import InputController
import time
from PIL import Image

def test_groq_chat():
    """测试Groq聊天功能"""
    controller = GroqController()
    
    # 测试简单的聊天
    messages = [
        {
            "role": "user",
            "content": "你好，请简单介绍一下你自己。"
        }
    ]
    
    response = controller.chat(messages)
    assert isinstance(response, str)
    assert len(response) > 0
    print(f"聊天回复: {response}")

def test_groq_image_analysis():
    """测试Groq图像分析功能"""
    groq_controller = GroqController()
    input_controller = InputController()
    
    # 等待2秒，给用户时间准备
    print("2秒后开始截图进行分析...")
    time.sleep(2)
    
    # 获取屏幕截图
    screenshot = input_controller.screenshot()
    
    # 分析图像
    result = groq_controller.analyze_image(
        image=screenshot,
        prompt="请详细描述这个界面截图中的内容，包括界面布局、文本内容和视觉元素。请用中文回答。"
    )
    
    assert isinstance(result, str)
    assert len(result) > 0
    print(f"\n分析结果:\n{result}")

if __name__ == "__main__":
    # 运行单个测试
    test_groq_image_analysis() 