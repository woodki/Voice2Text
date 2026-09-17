import tkinter as tk
from tkinter import filedialog, ttk
import threading
import os
import logging


logger = logging.getLogger(__name__)

# 保存用户选择的录音路径
audio_path = ""

last_md_path = ""

language_var = None

ai_correct_var = None

output_folder_var = None

# GUI更新函数
def update_status(message):

    status_label.config(
        text=message
    )

# 打开保存 Markdown 文件的文件夹
def open_output_folder():

    # 获取 Markdown 文件所在的文件夹
    folder_path = os.path.dirname(
        last_md_path
    )

    # 打开文件夹
    os.startfile(folder_path)

# 定义“选择录音”函数
def choose_audio():

    global audio_path
    global last_md_path

    audio_path = filedialog.askopenfilename(
        title="请选择录音文件",
        filetypes=[
            ("Audio Files", "*.m4a *.mp3 *.wav"),
            ("All Files", "*.*")
        ]
    )

    # 如果用户没有选择文件，直接结束
    if audio_path == "":
        return

    # 从完整路径中获取文件名
    audio_name = os.path.basename(
        audio_path
    )

    # 清除上一次生成的 Markdown 路径
    last_md_path = ""

    file_label.config(
        text=f"当前文件：{audio_name}"
    )

    # 清空上一次的识别结果
    result_text.delete(
        "1.0",
        tk.END
    )

    # 清空上一次的保存位置
    save_label.config(
        text="保存位置：暂无"
    )

    # 状态恢复为等待
    status_label.config(
        text="等待转换"
    )

    # 新录音还没有生成 Markdown，所以禁用打开文件夹按钮
    open_button.config(
        state=tk.DISABLED
    )


def choose_output_folder():
    folder = filedialog.askdirectory(
        title="请选择 Markdown 保存文件夹"
    )

    # 用户点取消时，不修改原来的选择
    if folder == "":
        return

    output_folder_var.set(folder)

    output_folder_label.config(
        text=f"输出目录：{folder}"
    )


# 定义“开始录音转文字”函数
def start_convert(service):

    if audio_path == "":
        status_label.config(
            text="请先选择录音"
        )
        return

    selected_output_folder = output_folder_var.get()

    if selected_output_folder == "":
        status_label.config(
            text="请选择输出文件夹"
        )
        return

    logger.info(
        "用户开始转换"
    )

    status_label.config(
        text="正在转换..."
    )
    # 转换过程中禁用按钮
    convert_button.config(
        state=tk.DISABLED
    )

    # 在主线程读取 GUI 变量
    selected_language = language_var.get()
    use_ai_correct = ai_correct_var.get()
    selected_output_folder = output_folder_var.get()
    api_key = api_key_var.get()

    thread = threading.Thread(
        target=convert_task,
        args=(
            service,
            selected_language,
            use_ai_correct,
            selected_output_folder,
            api_key
        )
    )

    thread.start()


def convert_task(
        service,
        selected_language,
        use_ai_correct,
        selected_output_folder,
        api_key
):
    try:
        logger.info("开始语音转换")

        text, corrected_text, md_path, ai_error = service.process(
            audio_path,
            selected_language,
            use_ai_correct,
            selected_output_folder,
            api_key
        )

        window.after(
            0,
            update_result,
            text,
            corrected_text,
            md_path,
            ai_error
        )

    except Exception:
        logger.error(
            "转换失败",
            exc_info=True
        )

        window.after(
            0,
            update_error,
            "转换失败，请查看控制台错误信息。"
        )

def update_error(error_message):
    status_label.config(
        text=f"转换失败：{error_message}"
    )

    # 恢复按钮
    convert_button.config(
        state=tk.NORMAL
    )

def update_result(text, corrected_text, md_path, ai_error):
    global last_md_path

    # 保存最近生成的 Markdown 路径
    last_md_path = md_path

    # 清空旧结果
    result_text.delete(
        "1.0",
        tk.END
    )

    # 显示新结果
    result_text.insert(
        tk.END,
        text
    )

    # 清空旧的 AI 纠错结果
    corrected_text_box.delete(
        "1.0",
        tk.END
    )

    # 显示新的 AI 纠错结果
    if corrected_text is not None:
        corrected_text_box.insert(
            tk.END,
            corrected_text
        )

        # 更新状态
        status_label.config(
            text=f"转换完成"
        )

    elif ai_error is not None:
        corrected_text_box.insert(
            tk.END,
            f"AI 纠错失败：{ai_error}\n原始转写已正常保存。"
        )

        status_label.config(
            text="转换完成（AI 纠错失败）"
        )

    else:
        status_label.config(
            text="转换完成"
        )

    # 显示 Markdown 保存位置
    save_label.config(
        text=f"保存位置：{md_path}"
    )

    # 恢复按钮
    convert_button.config(
        state=tk.NORMAL
    )

    open_button.config(
        state=tk.NORMAL
    )

def start_gui(service):
    global window
    global file_label
    global status_label
    global result_text
    global convert_button
    global save_label
    global open_button
    global language_var
    global ai_correct_var
    global api_key_var
    global corrected_text_box
    global output_folder_var
    global output_folder_label


    window = tk.Tk()

    window.title(
        "Voice2Text"
    )

    window.geometry(
        "600x600"
    )

    # 字体设置
    title_font = (
        "Microsoft YaHei UI",
        20,
        "bold"
    )

    normal_font = (
        "Microsoft YaHei UI",
        11
    )

    button_font = (
        "Microsoft YaHei UI",
        11
    )

    # 软件标题
    title_label = tk.Label(
        window,
        text="Voice2Text",
        font=title_font
    )
    title_label.pack(
        pady=20
    )

    # 文件选择区域
    file_frame = tk.Frame(
        window
    )
    file_frame.pack(
        pady=10
    )

    choose_button = tk.Button(
        file_frame,
        text="选择录音文件",
        command=choose_audio,
        font=button_font
    )
    file_label = tk.Label(
        file_frame,
        text="当前文件：未选择",
        font=normal_font
    )

    choose_button.pack(
        side=tk.LEFT,
        padx=5
    )
    file_label.pack(
        side=tk.LEFT,
        padx=5
    )

    # 输出文件夹选择区域
    output_frame = tk.Frame(
        window
    )
    output_frame.pack(
        pady=5
    )

    output_folder_var = tk.StringVar(
        value=""
    )

    output_button = tk.Button(
        output_frame,
        text="选择输出文件夹",
        command=choose_output_folder,
        font=button_font
    )

    output_folder_label = tk.Label(
        output_frame,
        text="输出目录：未选择",
        font=normal_font
    )

    output_button.pack(
        side=tk.LEFT,
        padx=5
    )

    output_folder_label.pack(
        side=tk.LEFT,
        padx=5
    )

    # 语言选择区域
    language_frame = tk.Frame(
        window
    )
    language_frame.pack(
        pady=5
    )

    language_label = tk.Label(
        language_frame,
        text="录音语言：",
        font=normal_font
    )

    language_var = tk.StringVar(
        value="自动检测"
    )

    language_menu = tk.OptionMenu(
        language_frame,
        language_var,
        "自动检测",
        "中文",
        "English"
    )

    language_menu.config(
        font=normal_font
    )

    language_label.pack(
        side=tk.LEFT,
        padx=5
    )

    language_menu.pack(
        side=tk.LEFT,
        padx=5
    )

    # AI纠错开关
    ai_correct_var = tk.BooleanVar(
        value=False
    )

    # API-KEY StringVar
    api_key_var = tk.StringVar()

    ai_correct_check = tk.Checkbutton(
        language_frame,
        text="英语 AI 纠错",
        variable=ai_correct_var,
        font=normal_font
    )

    # 创建API-KEY输入框
    api_key_entry = tk.Entry(
        language_frame,
        textvariable=api_key_var,
        show="*",
        width=30
    )

    api_key_entry.pack(
        side=tk.LEFT,
        padx=10
    )

    ai_correct_check.pack(
        side=tk.LEFT,
        padx=10
    )

    # 操作按钮区域
    action_frame = tk.Frame(
        window
    )
    action_frame.pack(
        pady=10
    )

    convert_button = tk.Button(
        action_frame,
        text="开始转换",
        command=lambda: start_convert(service),
        width=12,
        font=button_font
    )

    # 创建打开保存着markdown文件的文件夹的按钮
    open_button = tk.Button(
        action_frame,
        text="打开文件夹",
        command=open_output_folder,
        state=tk.DISABLED,
        width=12,
        font=button_font
    )

    convert_button.pack(
        side=tk.LEFT,
        padx=5
    )
    open_button.pack(
        side=tk.LEFT,
        padx=5
    )

    # 状态信息区域
    info_frame = tk.Frame(
        window
    )
    info_frame.pack(
        pady=10
    )

    status_label = tk.Label(
        info_frame,
        text="等待操作",
        font=normal_font
    )
    status_label.pack()

    # 显示 Markdown 保存位置
    save_label = tk.Label(
        info_frame,
        text="保存位置：暂无",
        font=normal_font
    )
    save_label.pack()

    # 识别结果标题
    result_label = tk.Label(
        window,
        text="识别结果",
        font=normal_font
    )

    result_label.pack(
        pady=(10, 0)
    )

    # 创建结果标签页
    result_notebook = ttk.Notebook(
        window
    )

    result_notebook.pack(
        pady=10,
        fill=tk.BOTH,
        expand=True
    )

    # 创建文本区域和滚动条的容器
    # 识别结果区域
    result_frame = tk.Frame(
        result_notebook
    )

    result_notebook.add(
        result_frame,
        text="原始转写"
    )

    # 创建 AI 纠错标签页
    corrected_frame = tk.Frame(
        result_notebook
    )

    result_notebook.add(
        corrected_frame,
        text="AI 纠错"
    )

    # 显示 AI 纠错结果
    corrected_text_box = tk.Text(
        corrected_frame,
        height=10,
        width=60,
        font=normal_font
    )

    corrected_text_box.pack(
        fill=tk.BOTH,
        expand=True
    )

    # 显示识别结果
    result_text = tk.Text(
        result_frame,
        height=10,
        width=60,
        font=normal_font
    )

    result_text.pack(
        side=tk.LEFT,
        fill=tk.BOTH,
        expand=True
    )

    # 创建垂直滚动条
    scrollbar = tk.Scrollbar(
        result_frame
    )

    scrollbar.pack(
        side=tk.RIGHT,
        fill=tk.Y
    )

    # Text滚动时，同步滚动条
    result_text.config(
        yscrollcommand=scrollbar.set
    )

    # 拖动滚动条时，控制Text上下移动
    scrollbar.config(
        command=result_text.yview
    )


    window.mainloop()