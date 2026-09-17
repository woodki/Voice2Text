# Voice2Text

Voice2Text 是一个本地桌面语音转写工具，支持将语音/录音文件转换为文本，并保存为 Markdown。

它也可以用于英语口语练习：用户可以输入 Gemini API Key 开启 AI 纠错，对英文转写结果进行修正和润色，使表达更加自然、流畅。

## 核心功能

- **中英文语音转写**：使用 Fun-ASR-Nano 模型将语音/录音转换为文本。
- **语言选择**：支持自动检测、中文、英文三种语言模式。
- **AI 英语纠错**：用户可输入 Gemini API Key 开启 AI 纠错，修正英文表达中的错误，并提供更加自然、流畅的表达建议。
- **Markdown 保存**：转写结果以 Markdown 格式保存到用户自定义的文件夹中。
- **文件名冲突处理**：当输出文件重名时，自动在文件名后添加序号，避免覆盖已有文件。
- **转换时间记录**：生成的 Markdown 文件中会记录转换时间。

## 技术栈

- **Python**：项目主要开发语言
- **Tkinter**：桌面 GUI
- **Fun-ASR-Nano**：当前默认 ASR 模型，用于中英文语音转写
- **Whisper**：早期使用的转写方案，目前保留作为备用实现
- **PyTorch + CUDA**：模型加载与 GPU 推理
- **Gemini API**：英文纠错与表达优化
- **pytest**：自动化测试
- **PyInstaller**：Windows 应用打包

## 项目结构

```
src/voice2text/
├── main.py
├── gui.py
├── config.py
├── logging_config.py
├── text_processing.py
│
├── transcription/
│   ├── funasr_nano_transcriber.py   # 当前默认的 Fun-ASR-Nano 转写实现
│   └── whisper_transcriber.py       # 保留的 Whisper 转写实现
│
├── ai/
│   └── gemini_client.py             # Gemini API 客户端
│
├── english_correction/
│   └── corrector.py                 # 英语纠错
│
├── application/
│   └── service.py                   # 应用流程编排
│
└── output/
    └── markdown_writer.py            # Markdown 输出
```

## 安装与运行

### 环境要求

- Python 3.12+
- Windows
- NVIDIA GPU + CUDA（推荐用于模型推理）

### 1. 创建虚拟环境

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. 安装项目依赖

```
pip install -e .
```

如需使用 PyInstaller 打包 Windows 应用，可安装额外的构建依赖：

```
pip install -e ".[build]"
```

### 3. 启动应用

```
python -m voice2text.main
```

### 4. 使用

1. 在 GUI 中选择需要转写的语音/录音文件。
2. 选择自动检测、中文或英文语言模式。
3. 如需使用 AI 英语纠错，在 GUI 中输入自己的 Gemini API Key 并开启 AI 纠错。
4. 选择输出文件夹并开始转换。
5. 转写结果将以 Markdown 格式保存到指定文件夹。

## 测试

项目使用 pytest 进行自动化测试。

```
pytest
```

当前测试结果：

```
9 passed
```