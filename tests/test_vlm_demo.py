from src.vlm_controller import VLMController
from src.input_controller import InputController
import time

def main():
    # 创建控制器实例
    vlm = VLMController(model_size="6b")  # 使用6B模型
    input_controller = InputController()
    
    # 等待用户准备
    print('2秒后开始截图...')
    time.sleep(2)
    
    # 获取屏幕截图
    print('\n正在截图...')
    screenshot = input_controller.screenshot()
    
    # 准备一些分析任务
    tasks = [
        "描述这个界面的主要内容和布局",
        "找出界面中所有的按钮和可点击元素",
        "分析界面的设计风格和用户体验",
    ]
    
    # 逐个执行分析任务
    for i, prompt in enumerate(tasks, 1):
        print(f'\n任务 {i}: {prompt}')
        print('-' * 50)
        
        # 分析图像
        response = vlm.analyze_image(
            image=screenshot,
            prompt=prompt,
            temperature=0.7,  # 可以调整以控制输出的创造性
            top_p=0.9,       # 可以调整以控制输出的多样性
        )
        
        print(f'分析结果:\n{response}\n')
        print('-' * 50)
        
    # 演示如何切换到更大的模型
    print('\n切换到17B模型...')
    vlm.change_model_size("17b")
    
    # 使用更大的模型进行一次分析
    prompt = "总结这个界面的整体设计理念和可用性"
    print(f'\n使用17B模型分析:\n{prompt}')
    print('-' * 50)
    
    response = vlm.analyze_image(
        image=screenshot,
        prompt=prompt,
        temperature=0.7,
        top_p=0.9,
    )
    
    print(f'分析结果:\n{response}')

if __name__ == '__main__':
    main() 