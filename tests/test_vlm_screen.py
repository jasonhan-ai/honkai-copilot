from src.vlm_controller import VLMController
from src.input_controller import InputController
import time

def main():
    # 创建控制器实例
    vlm = VLMController()  # 使用默认配置
    input_controller = InputController()
    
    # 等待用户准备
    print('2秒后开始截图...')
    time.sleep(2)
    
    # 获取屏幕截图
    print('\n正在截图...')
    screenshot = input_controller.screenshot()
    
    print('\n开始分析屏幕内容...')
    print('-' * 50)
    
    # 分析屏幕内容
    response = vlm.analyze_image(
        image=screenshot,
        max_length=128,  # 适当的长度限制
        num_blocks=3,    # 将屏幕分成3x3=9块
    )
    
    print(f'分析结果:\n{response}\n')
    print('-' * 50)

if __name__ == '__main__':
    main() 