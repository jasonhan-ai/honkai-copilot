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
    prompt = """请仔细分析这个界面的内容，告诉我：
1. 当前界面显示的主要内容和布局
2. 所有可见的文本信息
3. 界面中的按钮、图标和其他交互元素
4. 界面的整体风格和设计特点
请尽可能详细地描述。"""

    response = vlm.analyze_image(
        image=screenshot,
        prompt=prompt,
        max_length=512,
        num_beams=5,
        temperature=0.7,
        num_blocks=2,  # 将屏幕分成2x2=4块
    )
    
    print(f'分析结果:\n{response}\n')
    print('-' * 50)

if __name__ == '__main__':
    main() 