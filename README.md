# Honkai Copilot

一个基于 Groq API 的崩坏：星穹铁道游戏辅助工具，提供智能对话和图像分析功能。

```
  _    _                 _    _____                      _ _       _   
 | |  | |               | |  / ____|                    | (_)     | |  
 | |__| | ___  _ __ ___ | | | |     ___  _ __ ___  _ __ | |_ _ __ | |_ 
 |  __  |/ _ \| '_ ` _ \| | | |    / _ \| '_ ` _ \| '_ \| | | '_ \| __|
 | |  | | (_) | | | | | | | | |___| (_) | | | | | | |_) | | | | | | |_ 
 |_|  |_|\___/|_| |_| |_|_|  \_____\___/|_| |_| |_| .__/|_|_|_| |_|\__|
                                                   | |                  
                                                   |_|                  
```

## 功能特点

- **智能对话**：基于 Groq API 的智能对话系统，支持自然语言交互
- **图像分析**：自动识别游戏界面元素，提供智能操作建议
- **语音交互**：支持语音输入和输出，提供更自然的交互体验
- **按钮识别**：自动识别并点击游戏中的按钮，如"再来一次"、"初学者手册"等
- **屏幕变化检测**：智能检测屏幕变化，确保操作成功

## 安装依赖

```bash
pip install -r requirements.txt
```

## 环境配置

1. 创建 `.env` 文件并配置以下环境变量：
```
GROQ_API_KEY=your_api_key_here
```

## 使用示例

### 智能对话
```python
from src.groq_controller import GroqController

controller = GroqController()
response = controller.chat("你好，请介绍一下自己")
print(response)
```

### 图像分析
```python
from src.groq_controller import GroqController
from PIL import Image

controller = GroqController()
image = Image.open("screenshot.png")
result = controller.analyze_image(image, "请分析这张图片中的游戏界面")
print(result)
```

### 语音交互
```python
from src.tts_controller import TTSController

tts = TTSController()
tts.speak("欢迎使用Honkai Copilot")
```

### 按钮点击
```python
from scripts.retry_button_clicker import RetryButtonClicker

# 点击"再来一次"按钮
clicker = RetryButtonClicker()
clicker.click_button()

# 点击"初学者手册"按钮
clicker = RetryButtonClicker(button_description="初学者手册")
clicker.click_button()
```

## 项目结构

```
honkai-copilot/
├── src/
│   ├── groq_controller.py    # Groq API 控制器
│   ├── tts_controller.py     # 语音合成控制器
│   └── speech_controller.py  # 语音识别控制器
├── scripts/
│   └── retry_button_clicker.py  # 按钮点击脚本
├── tests/
│   ├── test_groq_controller.py
│   ├── test_tts_controller.py
│   └── test_speech_controller.py
├── requirements.txt          # 项目依赖
└── README.md                # 项目说明
```

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License 