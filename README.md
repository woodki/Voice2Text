# Voice2Text

English | [中文](README.zh-CN.md)

Voice2Text is a local desktop speech-to-text application that converts speech and audio recordings into text and saves the results as Markdown files.

It can also be used for English speaking practice. Users can enter their own Gemini API Key to enable AI-powered correction, which corrects errors in English transcriptions and provides suggestions for more natural and fluent expressions.

## Core Features

- **Chinese and English Speech Transcription**: Uses the Fun-ASR-Nano model to transcribe speech and audio recordings into text.
- **Language Selection**: Supports three language modes: automatic detection, Chinese, and English.
- **AI-powered English Correction**: Users can enter their own Gemini API Key to enable AI correction, correct errors in English transcriptions, and receive suggestions for more natural and fluent expressions.
- **Markdown Output**: Saves transcription results as Markdown files in a user-selected folder.
- **Filename Conflict Handling**: Automatically adds a sequence number to duplicate filenames to prevent existing files from being overwritten.
- **Conversion Time Recording**: Records the conversion time in the generated Markdown file.

## Tech Stack

- **Python**: Primary programming language
- **Tkinter**: Desktop GUI
- **Fun-ASR-Nano**: Current default ASR model for Chinese and English speech transcription
- **Whisper**: Previously used transcription solution, currently retained as a backup implementation
- **PyTorch + CUDA**: Model loading and GPU inference
- **Gemini API**: English correction and expression refinement
- **pytest**: Automated testing
- **PyInstaller**: Windows application packaging

## Project Structure

```text
src/voice2text/
├── main.py
├── gui.py
├── config.py
├── logging_config.py
├── text_processing.py
│
├── transcription/
│   ├── funasr_nano_transcriber.py   # Current default Fun-ASR-Nano transcription implementation
│   └── whisper_transcriber.py       # Retained Whisper transcription implementation
│
├── ai/
│   └── gemini_client.py             # Gemini API client
│
├── english_correction/
│   └── corrector.py                 # English correction
│
├── application/
│   └── service.py                   # Application workflow orchestration
│
└── output/
    └── markdown_writer.py           # Markdown output
```

## Installation & Usage

### Requirements

- Python 3.12+
- Windows
- NVIDIA GPU + CUDA (recommended for model inference)

### 1. Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```powershell
pip install -e .
```

To package the application for Windows with PyInstaller, install the optional build dependencies:

```powershell
pip install -e ".[build]"
```

### 3. Run the Application

```powershell
python -m voice2text.main
```

### 4. Usage

1. Select a speech or audio recording file in the GUI.
2. Choose automatic detection, Chinese, or English as the language mode.
3. To use AI-powered English correction, enter your own Gemini API Key in the GUI and enable AI correction.
4. Select an output folder and start the conversion.
5. The transcription result will be saved as a Markdown file in the selected folder.

## Testing

The project uses pytest for automated testing.

```powershell
pytest
```

Current test result:

```text
9 passed
```