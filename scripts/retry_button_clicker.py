import os
import time
from PIL import ImageGrab
from src.groq_controller import GroqController
from src.input_controller import InputController
import pyautogui
import json

class RetryButtonClicker:
    def __init__(self):
        self.groq = GroqController()
        self.input = InputController()
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 1.0
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"当前屏幕分辨率: {self.screen_width}x{self.screen_height}")
      

    def capture_screen(self):
        """捕获当前屏幕"""
        screenshot = ImageGrab.grab()
        return screenshot

    def analyze_screen(self, image):
        """分析屏幕内容，找出重试按钮位置"""
        prompt = """请仔细分析这张图片，找出"再来一次"按钮的精确位置。

要求：
1. 按钮通常位于屏幕底部区域
2. 按钮文字为"再来一次"或类似的重试文字
3. 坐标应该是按钮的中心点位置
4. 坐标值应该是0-1之间的相对位置，精确到小数点后5位

请严格按照以下格式返回结果：
x: 相对位置
y: 相对位置

如果没有找到按钮，只返回：未找到按钮

注意：即使按钮不是很明显，只要能看到类似"再来一次"的文字，也请尽量给出位置。
请不要返回任何额外的描述性文字，只返回坐标值或未找到按钮的提示。"""
        
        result = self.groq.analyze_image(image, prompt)
        return result

    def parse_coordinates(self, result):
        """解析坐标结果"""
        try:
            # 查找包含坐标的行
            lines = result.split('\n')
            x = None
            y = None
            for line in lines:
                line = line.strip()
                if ':' not in line:
                    continue
                key, value = line.split(':', 1)
                key = key.strip().lower()
                if key == 'x':
                    try:
                        x = float(value.strip())
                    except:
                        continue
                elif key == 'y':
                    try:
                        y = float(value.strip())
                    except:
                        continue
            
            if x is not None and y is not None:
                # 将相对坐标转换为绝对坐标
                absolute_x = int(x * self.screen_width)
                absolute_y = int(y * self.screen_height)
  
                return (absolute_x, absolute_y)
            return None
        except Exception as e:
            print(f"解析坐标时出错: {str(e)}")
            return None

    def click_retry_button(self):
        """执行完整的点击流程"""
        print("开始捕获屏幕...")
        screenshot = self.capture_screen()
        
        print("分析屏幕内容...")
        result = self.analyze_screen(screenshot)
        print(f"分析结果: {result}")
        
        coordinates = self.parse_coordinates(result)
        if coordinates:
            x, y = coordinates
            print(f"找到按钮位置: ({x}, {y})")
            print("移动鼠标并点击...")
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            print("点击完成")
            

        else:
            print("未找到按钮位置")

if __name__ == "__main__":
    clicker = RetryButtonClicker()
    clicker.click_retry_button() 