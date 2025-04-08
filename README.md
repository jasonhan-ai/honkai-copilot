# Honkai Copilot

## 项目简介

Honkai Copilot 是一个基于 Python 的崩坏3游戏辅助工具，集成了语音识别、图像分析和智能对话功能，旨在提供更智能的游戏体验。

## 主要功能

### 1. 语音识别与控制
- 支持实时语音输入识别
- 可自定义录音时长和参数
- 支持多种语言识别
- 自动清理临时文件

### 2. 图像分析与识别
- 实时屏幕内容分析
- 智能按钮定位
- 自动点击功能
- 支持坐标校准

### 3. 智能对话系统
- 基于 Groq API 的智能对话
- 支持图像内容分析
- 多轮对话支持
- 上下文理解

## 技术栈

- Python 3.8+
- SpeechRecognition - 语音识别
- PyAutoGUI - 自动化控制
- Groq API - 智能对话
- Pillow - 图像处理

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/jasonhan-ai/honkai-copilot.git
cd honkai-copilot
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的 API 密钥
```

## 使用说明

### 语音识别
```python
from src.speech_controller import SpeechController

controller = SpeechController()
text = controller.recognize_from_microphone(duration=5)  # 录音5秒
print(f"识别结果: {text}")
```

### 按钮点击
```python
from scripts.retry_button_clicker import RetryButtonClicker

clicker = RetryButtonClicker()
clicker.click_retry_button()  # 自动点击"再来一次"按钮
```

### 智能对话
```python
from src.groq_controller import GroqController

controller = GroqController()
response = controller.chat("分析当前屏幕内容")
print(f"AI回复: {response}")
```

## 项目结构

```
honkai-copilot/
├── src/
│   ├── speech_controller.py    # 语音识别控制器
│   ├── groq_controller.py      # Groq API 控制器
│   └── utils.py                # 工具函数
├── scripts/
│   ├── retry_button_clicker.py # 按钮点击器
│   └── mouse_position.py       # 鼠标位置跟踪器
├── tests/
│   ├── test_speech_controller.py
│   └── test_groq_controller.py
├── requirements.txt            # 项目依赖
└── README.md                   # 项目说明
```

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 项目维护者：Jason Han
- 邮箱：jasonhan@example.com

## 致谢

- [SpeechRecognition](https://github.com/Uberi/speech_recognition)
- [PyAutoGUI](https://github.com/asweigart/pyautogui)
- [Groq API](https://groq.com/) 