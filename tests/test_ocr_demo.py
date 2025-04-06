from src.input_controller import InputController
import time

def main():
    # 创建控制器实例
    controller = InputController()
    
    # 等待2秒，让用户准备
    print('2秒后开始截图...')
    time.sleep(2)
    
    # 执行全屏OCR
    print('\n开始OCR识别...')
    results = controller.ocr_screen()
    
    # 输出结果
    print(f'\n共检测到 {len(results)} 个文本区域:')
    for bbox, text, confidence in results:
        print(f'\n文本: {text}')
        print(f'位置: {bbox}')
        print(f'置信度: {confidence:.2f}')
        print('-' * 50)

if __name__ == '__main__':
    main() 