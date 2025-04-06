from src.input_controller import InputController
import time

def main():
    # 创建控制器实例
    controller = InputController()
    
    # 等待3秒，给用户时间切换窗口
    print("程序将在3秒后开始运行...")
    time.sleep(3)
    
    # 获取并打印当前鼠标位置
    x, y = controller.get_mouse_position()
    print(f"当前鼠标位置: ({x}, {y})")
    
    # 移动鼠标到屏幕中心
    center_x = controller.screen_width // 2
    center_y = controller.screen_height // 2
    print(f"移动鼠标到屏幕中心: ({center_x}, {center_y})")
    controller.move_mouse(center_x, center_y)
    
    # 相对移动示例
    print("相对当前位置移动鼠标 100 像素")
    controller.move_mouse_relative(100, 0)
    
    # 键盘输入示例
    print("模拟键盘输入...")
    controller.type_string("Hello, World!")
    
    # 组合键示例
    print("按下Command+A组合键")
    controller.hotkey('command', 'a')
    
    print("示例运行完成！")

if __name__ == "__main__":
    main() 