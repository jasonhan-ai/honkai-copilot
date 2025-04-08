import pyautogui
import time

class MousePositionTracker:
    def __init__(self):
        # 设置pyautogui的安全设置
        pyautogui.FAILSAFE = True
        # 获取屏幕尺寸
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"当前屏幕分辨率: {self.screen_width}x{self.screen_height}")

    def track_position(self, interval=0.1):
        """持续跟踪并打印鼠标位置"""
        print("开始跟踪鼠标位置...")
        print("按 Ctrl+C 停止跟踪")
        try:
            while True:
                x, y = pyautogui.position()
                print(f"当前鼠标位置: x={x}, y={y}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n停止跟踪")

    def get_current_position(self):
        """获取当前鼠标位置"""
        x, y = pyautogui.position()
        print(f"当前鼠标位置: x={x}, y={y}")
        return (x, y)

if __name__ == "__main__":
    tracker = MousePositionTracker()
    # 持续跟踪模式
    # tracker.track_position()
    
    # 单次获取模式
    tracker.get_current_position() 