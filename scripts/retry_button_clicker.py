import os
import time
from PIL import ImageGrab, ImageChops
from src.groq_controller import GroqController
from src.input_controller import InputController
import pyautogui
import json

class RetryButtonClicker:
    def __init__(self, button_description="再来一次"):
        self.groq = GroqController()
        self.input = InputController()
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 1.0
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"当前屏幕分辨率: {self.screen_width}x{self.screen_height}")
        # 设置按钮描述
        self.button_description = button_description
      
    def capture_region_around_cursor(self):
        """截取鼠标位置附近的区域图片，大小为屏幕的四分之一"""
        # 获取当前鼠标位置
        x, y = pyautogui.position()
        
        # 计算区域大小（屏幕的四分之一）
        region_width = self.screen_width // 2
        region_height = self.screen_height // 2
        
        # 计算区域左上角坐标，确保区域在屏幕范围内
        left = max(0, x - region_width // 2)
        top = max(0, y - region_height // 2)
        
        # 如果区域超出屏幕右边界，调整左边界
        if left + region_width > self.screen_width:
            left = self.screen_width - region_width
            
        # 如果区域超出屏幕下边界，调整上边界
        if top + region_height > self.screen_height:
            top = self.screen_height - region_height
            
        # 截取区域图片
        region = (left, top, left + region_width, top + region_height)
        screenshot = ImageGrab.grab(region)
        
        return screenshot, (left, top)

    def compare_images(self, img1, img2, threshold=30):
        """比较两张图片的差异，返回差异程度（0-100）"""
        # 确保两张图片大小相同
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)
            
        # 计算差异
        diff = ImageChops.difference(img1, img2)
        
        # 转换为灰度图
        diff = diff.convert('L')
        
        # 计算差异像素的数量
        diff_pixels = sum(1 for pixel in diff.getdata() if pixel > threshold)
        total_pixels = img1.size[0] * img1.size[1]
        
        # 计算差异百分比
        diff_percentage = (diff_pixels / total_pixels) * 100
        
        return diff_percentage

    def capture_screen(self):
        """捕获当前屏幕"""
        screenshot = ImageGrab.grab()
        return screenshot

    def analyze_screen(self, image):
        """分析屏幕内容，找出按钮位置"""
        prompt = f"""请仔细分析这张图片，找出"{self.button_description}"按钮的精确位置。

要求：
1. 按钮通常位于屏幕底部区域
2. 按钮文字为"{self.button_description}"或类似的文字
3. 坐标应该是按钮的中心点位置
4. 坐标值应该是0-1之间的相对位置，精确到小数点后5位

请严格按照以下格式返回结果：
x: 相对位置
y: 相对位置

如果没有找到按钮，只返回：未找到按钮

注意：即使按钮不是很明显，只要能看到类似"{self.button_description}"的文字，也请尽量给出位置。
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

    def try_click_with_region(self, before_screenshot):
        """使用鼠标附近区域进行二次尝试"""
        print("开始二次尝试，使用鼠标附近区域...")
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
                print("移动鼠标并点击...")
                pyautogui.moveTo(x, y, duration=0.5)
                pyautogui.click()
                print("点击完成")
                
                # 等待2秒后再次截屏
                print("等待2秒后检查屏幕变化...")
                time.sleep(2)
                after_screenshot = self.capture_screen()
                
                # 比较前后屏幕的差异
                diff_percentage = self.compare_images(before_screenshot, after_screenshot)
                print(f"屏幕变化程度: {diff_percentage:.2f}%")
                
                return diff_percentage > 1
            return False
        except Exception as e:
            print(f"解析坐标时出错: {str(e)}")
            return False

    def click_button(self):
        """执行完整的点击流程"""
        print("开始捕获屏幕...")
        before_screenshot = self.capture_screen()
        
        print("分析屏幕内容...")
        result = self.analyze_screen(before_screenshot)
        print(f"分析结果: {result}")
        
        coordinates = self.parse_coordinates(result)
        if coordinates:
            x, y = coordinates
            print(f"找到按钮位置: ({x}, {y})")
            print("移动鼠标并点击...")
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            print("点击完成")
            
            # 等待2秒后再次截屏
            print("等待2秒后检查屏幕变化...")
            time.sleep(2)
            after_screenshot = self.capture_screen()
            
            # 比较前后屏幕的差异
            diff_percentage = self.compare_images(before_screenshot, after_screenshot)
            print(f"屏幕变化程度: {diff_percentage:.2f}%")
            
            # 如果变化程度超过阈值，认为点击成功
            if diff_percentage > 1:
                print("检测到明显的屏幕变化，点击成功")
            else:
                print("未检测到明显的屏幕变化，开始二次尝试...")
                # 使用鼠标附近区域进行二次尝试
                if self.try_click_with_region(before_screenshot):
                    print("二次尝试成功")
                else:
                    print("二次尝试失败")
        else:
            print("未找到按钮位置")

if __name__ == "__main__":
    # 测试点击"初学者手册"按钮
    clicker = RetryButtonClicker(button_description="初学者手册")
    clicker.click_button() 