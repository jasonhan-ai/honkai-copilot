import pytest
from src.groq_controller import GroqController
from src.input_controller import InputController
import time
from PIL import Image
import os


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
        prompt=open(".src/prompts/current_screen_info.txt", "r", encoding="utf-8").read().strip()
    )
    
    assert isinstance(result, str)
    assert len(result) > 0
    print(f"\n分析结果:\n{result}")

def test_groq_image_chat():
    """测试Groq图像分析和聊天的组合功能"""
    groq_controller = GroqController()
    input_controller = InputController()
    
    # 等待2秒，给用户时间准备
    print("2秒后开始截图进行分析...")
    time.sleep(2)
    
    # 获取屏幕截图
    screenshot = input_controller.screenshot()
    
    # 分析图像并发送到聊天ß
    image_analysis = groq_controller.analyze_image(
        image=screenshot,
        prompt=open(".src/prompts/current_screen_info.txt", "r", encoding="utf-8").read().strip()
    )
    
    # 构建消息列表
    messages = [
        {
            "role": "user",
            "content": f"这是一张截图的分析结果：\n{image_analysis}\n\n问题：截图中的内容是什么？请用中文简单汇总。"
        }
    ]
    
    # 发送到聊天接口获取总结
    response = groq_controller.chat(messages)
    
    assert isinstance(response, str)
    assert len(response) > 0
    print(f"\n图像分析结果:\n{image_analysis}")
    print(f"\n总结回复:\n{response}")

if __name__ == "__main__":
    # 运行单个测试
    test_groq_image_chat() 