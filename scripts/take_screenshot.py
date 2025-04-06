from src.input_controller import InputController
import time
from datetime import datetime

def main():
    # 创建控制器实例
    controller = InputController()
    
    # 等待2秒，给用户时间准备
    print("2秒后开始截图...")
    time.sleep(2)
    
    # 获取当前时间作为文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"downloads/screenshot_{timestamp}.png"
    
    # 截取屏幕
    print("正在截图...")
    screenshot = controller.screenshot()
    
    # 保存截图
    screenshot.save(filename)
    print(f"截图已保存到: {filename}")

if __name__ == "__main__":
    main() 