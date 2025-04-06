# Honkai Copilot

崩坏：星穹铁道游戏助手，基于计算机视觉和自然语言处理技术。
![image](https://github.com/user-attachments/assets/9e5f4a51-b164-4307-b129-039958afd30d)

## 功能特性

1. 屏幕内容分析
   - 使用InstructBLIP模型进行场景理解
   - 支持中英文场景描述
   - 可配置的分析参数

2. OCR文本识别
   - 基于EasyOCR引擎
   - 支持中英文识别
   - 支持全屏和区域识别

3. 输入控制
   - 键盘输入模拟
   - 鼠标移动和点击
   - 热键组合支持

4. Groq API集成
   - 使用meta-llama/llama-4-scout-17b-16e-instruct模型
   - 支持图像分析和文本聊天
   - 中文场景描述和总结
   - 可配置的生成参数（temperature、max_tokens等）

## 项目结构

```
.
├── assets/                # 资源文件
│   └── fonts/            # 字体文件
│       ├── README.md     # 字体说明
│       └── SimSun.ttf    # 宋体字体文件
│
├── examples/             # 示例代码
│   └── input_controller_demo.py  # 输入控制示例
│
├── src/                  # 源代码
│   ├── __init__.py
│   ├── input_controller.py   # 输入控制模块
│   ├── ocr_controller.py     # OCR识别模块
│   ├── vlm_controller.py     # 视觉语言模型控制器
│   └── groq_controller.py    # Groq API控制器
│
├── tests/                # 测试代码
│   ├── __init__.py
│   ├── test_input_controller.py  # 输入控制测试
│   ├── test_ocr_demo.py         # OCR功能测试
│   ├── test_vlm_demo.py         # VLM基础测试
│   ├── test_vlm_screen.py       # VLM屏幕分析测试
│   └── test_groq_controller.py  # Groq功能测试
│
├── .env                 # 环境变量配置
├── LICENSE              # MIT许可证
└── requirements.txt     # 项目依赖
```

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/jasonhan-ai/honkai-copilot.git
cd honkai-copilot
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate   # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
创建 `.env` 文件并添加以下内容：
```bash
GROQ_API_KEY=your_api_key_here  # 替换为你的Groq API密钥
```

## 使用示例

1. 运行输入控制示例：
```bash
python examples/input_controller_demo.py
```

2. 运行OCR识别测试：
```bash
python -m pytest tests/test_ocr_demo.py -v
```

3. 运行屏幕分析：
```bash
python tests/test_vlm_screen.py
```

4. 运行Groq功能测试：
```bash
python -m pytest tests/test_groq_controller.py -v
```

## 开发说明

1. 输入控制模块 (`input_controller.py`)
   - 提供键盘和鼠标操作的底层接口
   - 支持相对和绝对坐标移动
   - 支持组合键操作

2. OCR识别模块 (`ocr_controller.py`)
   - 封装EasyOCR引擎
   - 提供全屏和区域文本识别
   - 支持中英文识别配置

3. 视觉语言模型控制器 (`vlm_controller.py`)
   - 使用InstructBLIP模型进行场景理解
   - 支持自定义提示词
   - 可配置的生成参数

4. Groq API控制器 (`groq_controller.py`)
   - 使用meta-llama/llama-4-scout-17b-16e-instruct模型
   - 支持图像分析和文本聊天功能
   - 提供灵活的API参数配置
   - 支持多种分析场景和提示词

## 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。 
