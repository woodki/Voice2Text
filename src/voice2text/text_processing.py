
# 中文标点转换
def convert_punctuation(text):
    text = text.replace(",", "，")
    text = text.replace(".", "。")
    text = text.replace("?", "？")
    text = text.replace("!", "！")

    return text