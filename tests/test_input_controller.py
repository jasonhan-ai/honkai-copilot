import pytest
from src.input_controller import InputController
from src.ocr_controller import OCRController
import time
import os
from PIL import Image  # 用于验证截图
import pyautogui

@pytest.fixture
def controller():
    """创建一个禁用下载的控制器实例"""
    return InputController(download_enabled=False)

@pytest.fixture
def ocr_controller():
    """创建一个禁用下载的OCR控制器实例"""
    return OCRController(download_enabled=False)

def test_initialization(controller):
    """测试控制器初始化"""
    assert controller.screen_width > 0
    assert controller.screen_height > 0
    assert controller._ocr_controller is not None

def test_ocr_controller_initialization(ocr_controller):
    """测试OCR控制器初始化"""
    assert ocr_controller.model_dir is not None
    assert os.path.exists(ocr_controller.model_dir)

def test_mouse_position(controller):
    """测试获取鼠标位置"""
    x, y = controller.get_mouse_position()
    
    # 基本类型检查
    assert isinstance(x, int)
    assert isinstance(y, int)
    
    # 确保坐标非负
    assert x >= 0
    assert y >= 0
    
    # 在多显示器设置下，我们只需要确保坐标是合理的正数
    # 通常不会超过10000像素（即使是4K或8K显示器）
    assert x < 10000, f"鼠标X坐标 {x} 不合理"
    assert y < 10000, f"鼠标Y坐标 {y} 不合理"

def test_absolute_mouse_movement(controller):
    """测试鼠标绝对位置移动"""
    # 移动到主屏幕中心
    center_x = controller.screen_width // 2
    center_y = controller.screen_height // 2
    controller.move_mouse(center_x, center_y)
    time.sleep(0.5)
    
    x, y = controller.get_mouse_position()
    # 允许100像素的误差（考虑到多显示器和系统缩放）
    assert abs(x - center_x) < 100
    assert abs(y - center_y) < 100

def test_relative_mouse_movement(controller):
    """测试鼠标相对位置移动"""
    # 获取当前位置
    initial_x, initial_y = controller.get_mouse_position()
    
    # 测试相对移动
    x_offset = 100
    controller.move_mouse_relative(x_offset, 0)
    time.sleep(0.5)
    
    new_x, new_y = controller.get_mouse_position()
    # 验证X轴移动方向正确，Y轴变化不大
    assert new_x > initial_x
    assert abs(new_y - initial_y) < 100  # 增加容差

def test_click_operations(controller):
    """测试鼠标点击操作"""
    # 移动到主屏幕的安全位置
    safe_x = min(controller.screen_width - 100, 100)  # 避免移动到扩展屏幕
    safe_y = min(controller.screen_height - 100, 100)
    controller.move_mouse(safe_x, safe_y)
    time.sleep(0.5)
    
    # 测试各种点击
    controller.click()  # 测试单击
    controller.double_click()  # 测试双击
    controller.click(button='right')  # 测试右键点击
    
    # 由于点击操作难以验证结果，这里主要测试操作不会抛出异常

def test_keyboard_input(controller):
    """测试键盘输入"""
    # 测试单个按键
    controller.press_key('shift')
    
    # 测试组合键
    controller.hotkey('command', 'a')
    
    # 测试文本输入
    test_string = "Test123"
    controller.type_string(test_string)
    
    # 这些操作主要测试不会抛出异常

def test_screenshot(controller):
    """测试截图功能"""
    test_file = "test_screenshot.png"
    
    # 确保测试开始时文件不存在
    if os.path.exists(test_file):
        os.remove(test_file)
    
    try:
        # 尝试截图
        print(f"\n当前工作目录: {os.getcwd()}")
        screenshot = controller.screenshot(test_file)
        print(f"截图返回值: {screenshot}")
        print(f"文件是否存在: {os.path.exists(test_file)}")
        
        # 验证文件存在
        assert os.path.exists(test_file), f"截图文件 {test_file} 未能创建"
        
        # 验证文件是否为有效的图片
        with Image.open(test_file) as img:
            # 验证图片尺寸是否与屏幕尺寸匹配
            width, height = img.size
            print(f"图片尺寸: {width}x{height}")
            print(f"屏幕尺寸: {controller.screen_width}x{controller.screen_height}")
            assert width == controller.screen_width
            assert height == controller.screen_height
            
            # 验证图片模式（应该是RGB）
            print(f"图片模式: {img.mode}")
            assert img.mode in ('RGB', 'RGBA')
            
            # 验证图片不是空白的（至少有一些像素值不为0）
            pixels = list(img.getdata())
            non_zero_pixels = sum(1 for pixel in pixels if sum(pixel[:3]) > 0)
            print(f"非零像素数量: {non_zero_pixels}")
            assert any(sum(pixel[:3]) > 0 for pixel in pixels)
            
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

def test_screen_functions(controller):
    """测试屏幕相关功能"""
    # 测试获取像素颜色
    x, y = controller.get_mouse_position()
    color = controller.get_pixel_color(x, y)
    assert len(color) == 3
    assert all(isinstance(c, int) for c in color)
    assert all(0 <= c <= 255 for c in color)

def test_ocr_screen(controller):
    """测试全屏OCR功能"""
    # 执行全屏OCR
    results = controller.ocr_screen()
    
    # 验证返回格式
    assert isinstance(results, list)
    if results:  # 如果检测到文本
        for bbox, text, confidence in results:
            # 验证边界框格式
            assert isinstance(bbox, list)
            assert len(bbox) == 4  # 四个角点
            for point in bbox:
                assert isinstance(point, tuple)
                assert len(point) == 2  # x, y 坐标
                assert all(isinstance(coord, int) for coord in point)
            
            # 验证文本
            assert isinstance(text, str)
            assert len(text) > 0
            
            # 验证置信度
            assert isinstance(confidence, float)
            assert 0 <= confidence <= 1
            
        print(f"\n检测到 {len(results)} 个文本区域:")
        for bbox, text, confidence in results:
            print(f"文本: {text}")
            print(f"位置: {bbox}")
            print(f"置信度: {confidence:.2f}")
            print("---")

def test_ocr_region(controller):
    """测试区域OCR功能"""
    # 选择屏幕中心区域进行OCR
    region_width = 400
    region_height = 300
    x = controller.screen_width // 2 - region_width // 2
    y = controller.screen_height // 2 - region_height // 2
    
    # 执行区域OCR
    results = controller.ocr_region(x, y, region_width, region_height)
    
    # 验证返回格式
    assert isinstance(results, list)
    if results:  # 如果检测到文本
        for bbox, text, confidence in results:
            # 验证边界框在指定区域内
            for point in bbox:
                assert x <= point[0] <= x + region_width
                assert y <= point[1] <= y + region_height
            
            # 验证文本和置信度
            assert isinstance(text, str)
            assert isinstance(confidence, float)
            assert 0 <= confidence <= 1
            
        print(f"\n在区域 ({x}, {y}, {region_width}, {region_height}) 中检测到 {len(results)} 个文本:")
        for bbox, text, confidence in results:
            print(f"文本: {text}")
            print(f"位置: {bbox}")
            print(f"置信度: {confidence:.2f}")
            print("---")

def test_ocr_controller_recognize_image(ocr_controller):
    """测试OCR控制器的图像识别功能"""
    # 创建一个测试图像
    test_image = Image.new('RGB', (100, 30), color='white')
    
    # 执行OCR识别
    results = ocr_controller.recognize_image(test_image)
    
    # 验证返回格式
    assert isinstance(results, list)
    
    # 测试带区域参数的识别
    region = (10, 10, 80, 20)
    results_with_region = ocr_controller.recognize_image(test_image, region)
    assert isinstance(results_with_region, list) 