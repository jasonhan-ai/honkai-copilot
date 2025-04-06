import time
import pyautogui
import numpy as np
from typing import List, Tuple, Optional
from .ocr_controller import OCRController

# 设置pyautogui的安全特性
pyautogui.FAILSAFE = True  # 启用故障安全
pyautogui.PAUSE = 0.1  # 操作之间的默认延迟

class InputController:
    def __init__(self, download_enabled: bool = True):
        """
        初始化输入控制器
        
        Args:
            download_enabled: 是否允许下载模型文件，如果为False则使用本地模型
        """
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = pyautogui.size()
        # 初始化OCR控制器
        self._ocr_controller = OCRController(download_enabled=download_enabled)
    
    # 鼠标操作
    def move_mouse(self, x: int, y: int, duration: float = 0.2):
        """移动鼠标到指定位置"""
        pyautogui.moveTo(x, y, duration=duration)
    
    def move_mouse_relative(self, x_offset: int, y_offset: int, duration: float = 0.2):
        """相对当前位置移动鼠标"""
        pyautogui.moveRel(x_offset, y_offset, duration=duration)
    
    def click(self, x: int = None, y: int = None, button: str = 'left'):
        """点击指定位置，如果不指定位置则在当前位置点击"""
        if x is not None and y is not None:
            pyautogui.click(x, y, button=button)
        else:
            pyautogui.click(button=button)
    
    def double_click(self, x: int = None, y: int = None):
        """双击指定位置"""
        if x is not None and y is not None:
            pyautogui.doubleClick(x, y)
        else:
            pyautogui.doubleClick()
    
    def drag_to(self, x: int, y: int, duration: float = 0.2):
        """拖拽到指定位置"""
        pyautogui.dragTo(x, y, duration=duration)
    
    def get_mouse_position(self) -> tuple:
        """获取当前鼠标位置"""
        return pyautogui.position()
    
    # 键盘操作
    def press_key(self, key: str):
        """按下并释放一个键"""
        pyautogui.press(key)
    
    def hold_key(self, key: str):
        """按住一个键"""
        pyautogui.keyDown(key)
    
    def release_key(self, key: str):
        """释放一个键"""
        pyautogui.keyUp(key)
    
    def type_string(self, text: str, interval: float = 0.1):
        """输入一串文本"""
        pyautogui.write(text, interval=interval)
    
    def hotkey(self, *args):
        """组合键"""
        pyautogui.hotkey(*args)
    
    # 实用方法
    def screenshot(self, filename: str = None):
        """截取屏幕截图"""
        img = pyautogui.screenshot()
        if filename:
            img.save(filename)
        return img
    
    def get_pixel_color(self, x: int, y: int) -> tuple:
        """获取指定位置的像素颜色"""
        return pyautogui.pixel(x, y)
    
    def locate_on_screen(self, image_path: str, confidence: float = 0.9):
        """在屏幕上查找图像"""
        try:
            return pyautogui.locateOnScreen(image_path, confidence=confidence)
        except pyautogui.ImageNotFoundException:
            return None

    def ocr_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> List[Tuple[List[Tuple[int, int]], str, float]]:
        """
        对屏幕进行OCR识别
        
        Args:
            region: 可选的区域参数 (left, top, width, height)，如果不指定则对整个屏幕进行识别
        
        Returns:
            List of tuples, each containing:
            - List of coordinates [(x1,y1), (x2,y2), (x3,y3), (x4,y4)] for text bounding box
            - Detected text string
            - Confidence score
        """
        screenshot = self.screenshot()
        return self._ocr_controller.recognize_image(screenshot, region)

    def ocr_region(self, x: int, y: int, width: int, height: int) -> List[Tuple[List[Tuple[int, int]], str, float]]:
        """
        对指定区域进行OCR识别
        
        Args:
            x: 区域左上角的X坐标
            y: 区域左上角的Y坐标
            width: 区域宽度
            height: 区域高度
        
        Returns:
            List of tuples, each containing:
            - List of coordinates for text bounding box
            - Detected text string
            - Confidence score
        """
        return self.ocr_screen((x, y, width, height)) 