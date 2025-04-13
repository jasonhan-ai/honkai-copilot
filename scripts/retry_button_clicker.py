import os
import time
import json
import pyautogui
from PIL import Image
import numpy as np
from src.groq_controller import GroqController
from src.tts_controller import TTSController

class RetryButtonClicker:
    def __init__(self, button_description="再来一次"):
        """初始化按钮点击器"""
        self.button_description = button_description
        self.groq = GroqController()
        self.tts = TTSController()
        self.calibration_data = self.load_calibration()
        
    def load_calibration(self):
        """加载校准数据"""
        if os.path.exists('calibration.json'):
            with open('calibration.json', 'r') as f:
                return json.load(f)
        return None

    def save_calibration(self, data):
        """保存校准数据"""
        with open('calibration.json', 'w') as f:
            json.dump(data, f)

    def capture_screen(self):
        """捕获整个屏幕"""
        screenshot = pyautogui.screenshot()
        return screenshot

    def capture_region_around_cursor(self, region_size=400):
        """捕获鼠标光标周围的区域"""
        x, y = pyautogui.position()
        left = max(0, x - region_size // 2)
        top = max(0, y - region_size // 2)
        right = min(pyautogui.size().width, x + region_size // 2)
        bottom = min(pyautogui.size().height, y + region_size // 2)
        
        region = (left, top, right, bottom)
        screenshot = pyautogui.screenshot(region=region)
        return screenshot, (left, top)

    def compare_images(self, img1, img2):
        """比较两张图片的差异"""
        if img1.size != img2.size:
            return 100.0
        
        # 转换为numpy数组
        arr1 = np.array(img1)
        arr2 = np.array(img2)
        
        # 计算差异
        diff = np.abs(arr1 - arr2)
        diff_percentage = (np.sum(diff) / (arr1.size * 255)) * 100
        return diff_percentage

    def analyze_screen(self, screenshot):
        """分析屏幕内容，查找按钮位置"""
        # 将PIL图像转换为base64
        image_data = self.groq._encode_image(screenshot)
        
        # 构建提示词
        prompt = f"""请分析这张图片，找到"{self.button_description}"按钮的位置。
按钮通常位于屏幕底部，是一个明显的可点击区域。
请返回按钮中心的相对坐标，格式如下：
x: 相对位置 (0-1之间的小数，精确到3位)
y: 相对位置 (0-1之间的小数，精确到3位)
如果找不到按钮，请返回"未找到按钮"。
"""
        
        # 调用Groq API进行分析
        result = self.groq.analyze_image(image_data, prompt)
        return result

    def parse_coordinates(self, result):
        """解析坐标"""
        try:
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
                # 应用校准数据
                if self.calibration_data:
                    x_offset = self.calibration_data.get('x_offset', 0)
                    y_offset = self.calibration_data.get('y_offset', 0)
                    x += x_offset
                    y += y_offset
                
                # 将相对坐标转换为绝对坐标
                screen_width, screen_height = pyautogui.size()
                x = int(x * screen_width)
                y = int(y * screen_height)
                return x, y
            return None
        except Exception as e:
            print(f"解析坐标时出错: {str(e)}")
            return None

    def try_click_with_region(self, before_screenshot):
        """使用鼠标附近区域进行二次尝试"""
        print("开始二次尝试，使用鼠标附近区域...")
        self.tts.speak("开始二次尝试，使用鼠标附近区域")
        
        region_screenshot, (left, top) = self.capture_region_around_cursor()
        
        # 分析区域图片
        result = self.analyze_screen(region_screenshot)
        print(f"区域分析结果: {result}")
        
        # 直接解析相对坐标
        try:
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
                # 将相对坐标转换为区域内的绝对坐标
                region_width = region_screenshot.width
                region_height = region_screenshot.height
                x = left + int(x * region_width)
                y = top + int(y * region_height)
                print(f"找到按钮位置: ({x}, {y})")
                self.tts.speak(f"找到按钮位置，坐标：{x}，{y}")
                
                print("移动鼠标并点击...")
                self.tts.speak("移动鼠标并点击")
                pyautogui.moveTo(x, y, duration=0.5)
                pyautogui.click()
                print("点击完成")
                
                # 等待2秒后再次截屏
                print("等待2秒后检查屏幕变化...")
                self.tts.speak("等待检查屏幕变化")
                time.sleep(2)
                after_screenshot = self.capture_screen()
                
                # 比较前后屏幕的差异
                diff_percentage = self.compare_images(before_screenshot, after_screenshot)
                print(f"屏幕变化程度: {diff_percentage:.2f}%")
                
                if diff_percentage > 1:
                    self.tts.speak("点击成功")
                else:
                    self.tts.speak("点击失败")
                
                return diff_percentage > 1
            return False
        except Exception as e:
            print(f"解析坐标时出错: {str(e)}")
            self.tts.speak("解析坐标时出错")
            return False

    def click_button(self):
        """执行完整的点击流程"""
        print("开始捕获屏幕...")
        self.tts.speak("开始捕获屏幕")
        before_screenshot = self.capture_screen()
        
        print("分析屏幕内容...")
        self.tts.speak("分析屏幕内容")
        result = self.analyze_screen(before_screenshot)
        print(f"分析结果: {result}")
        
        coordinates = self.parse_coordinates(result)
        if coordinates:
            x, y = coordinates
            print(f"找到按钮位置: ({x}, {y})")
            self.tts.speak(f"找到按钮位置，坐标：{x}，{y}")
            
            print("移动鼠标并点击...")
            self.tts.speak("移动鼠标并点击")
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            print("点击完成")
            
            # 等待2秒后再次截屏
            print("等待2秒后检查屏幕变化...")
            self.tts.speak("等待检查屏幕变化")
            time.sleep(2)
            after_screenshot = self.capture_screen()
            
            # 比较前后屏幕的差异
            diff_percentage = self.compare_images(before_screenshot, after_screenshot)
            print(f"屏幕变化程度: {diff_percentage:.2f}%")
            
            # 如果变化程度超过阈值，认为点击成功
            if diff_percentage > 1:
                print("检测到明显的屏幕变化，点击成功")
                self.tts.speak("点击成功")
            else:
                print("未检测到明显的屏幕变化，开始二次尝试...")
                self.tts.speak("未检测到变化，开始二次尝试")
                # 使用鼠标附近区域进行二次尝试
                if self.try_click_with_region(before_screenshot):
                    print("二次尝试成功")
                    self.tts.speak("二次尝试成功")
                else:
                    print("二次尝试失败")
                    self.tts.speak("二次尝试失败")
        else:
            print("未找到按钮位置")
            self.tts.speak("未找到按钮位置")

if __name__ == "__main__":
    # 测试点击"初学者手册"按钮
    clicker = RetryButtonClicker(button_description="初学者手册")
    clicker.click_button() 