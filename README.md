# Honkai Copilot

Honkai Copilot 是一个基于计算机视觉和自然语言处理的游戏辅助工具，专门为《崩坏：星穹铁道》设计。它能够实时分析游戏界面，识别文本和界面元素，并提供智能辅助功能。

## 功能特性

### 输入控制
- 鼠标操作
  - 精确移动和点击
  - 相对位置移动
  - 拖拽操作
  - 获取鼠标位置
- 键盘操作
  - 按键输入
  - 组合键
  - 文本输入

### 屏幕分析
- OCR 文本识别
  - 全屏文本识别
  - 区域文本识别
  - 多语言支持（中文、英文）
- 视觉分析
  - 界面元素识别
  - 场景理解
  - 实时状态监测

### 智能辅助
- 自动化操作
- 场景识别
- 任务辅助

## 技术栈

- Python 3.13+
- PyAutoGUI：用于鼠标和键盘控制
- EasyOCR：用于文本识别
- Microsoft TrOCR：用于高精度文本识别和场景理解
- PyTorch：深度学习框架
- Transformers：用于视觉语言模型

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/jasonhan-ai/honkai-copilot.git
cd honkai-copilot
```

2. 创建并激活虚拟环境（推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```python
from src.input_controller import InputController
from src.vlm_controller import VLMController

# 创建控制器实例
input_ctrl = InputController()
vlm_ctrl = VLMController()

# 获取屏幕截图
screenshot = input_ctrl.screenshot()

# 分析屏幕内容
result = vlm_ctrl.analyze_image(screenshot)
print(result)
```

### OCR 文本识别

```python
# 全屏文本识别
results = input_ctrl.ocr_screen()
for bbox, text, confidence in results:
    print(f"文本: {text}")
    print(f"位置: {bbox}")
    print(f"置信度: {confidence}")

# 区域文本识别
region_results = input_ctrl.ocr_region(x=100, y=100, width=200, height=200)
```

## 开发指南

### 项目结构

```
honkai-copilot/
├── src/
│   ├── input_controller.py    # 输入控制模块
│   ├── ocr_controller.py      # OCR控制模块
│   └── vlm_controller.py      # 视觉语言模型控制模块
├── tests/
│   ├── test_input_controller.py
│   ├── test_ocr_demo.py
│   └── test_vlm_screen.py
├── requirements.txt
└── README.md
```

### 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试
python -m pytest tests/test_vlm_screen.py
```

## 注意事项

1. 首次运行时需要下载模型文件，请确保网络连接正常
2. 在 macOS 上首次运行时需要授予辅助功能权限
3. 建议在虚拟环境中运行以避免依赖冲突
4. 使用 GPU 加速时需要确保 CUDA 正确安装（如果可用）

## 系统要求

- Python 3.13+
- macOS/Windows/Linux
- 8GB+ RAM（使用GPU加速时推荐16GB+）
- 可选：NVIDIA GPU（用于加速模型推理）

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献指南

欢迎提交 Issue 和 Pull Request。在提交 PR 之前，请确保：

1. 代码符合 PEP 8 规范
2. 添加了适当的测试
3. 更新了文档
4. 所有测试都能通过

## 致谢

- [PyAutoGUI](https://github.com/asweigart/pyautogui)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [Microsoft TrOCR](https://huggingface.co/microsoft/trocr-base-handwritten)
- [Transformers](https://github.com/huggingface/transformers) 