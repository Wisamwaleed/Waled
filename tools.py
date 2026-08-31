import os

def calculate_math(expression: str) -> str:
    """أداة لحساب العمليات الحسابية بدقة."""
    try:
        result = eval(expression)
        return f"النتيجة الرياضية هي: {result}"
    except Exception as e:
        return f"حدث خطأ في الحساب: {e}"

def read_local_file(file_path: str) -> str:
    """أداة لقراءة محتوى أي ملف نصي على الحاسوب."""
    try:
        if not os.path.exists(file_path):
            return "الملف غير موجود."
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"فشل قراءة الملف: {e}"

agent_tools = {
    "calculate_math": calculate_math,
    "read_local_file": read_local_file
}

def reverse_text(text: str) -> str:
    """
    عكس النص المدخل.
    """
    return text[::-1]



def reverse_text(text: str) -> str:
    """
    Reverses the given input text.

    :param text: The text to be reversed.
    :return: The reversed text string.
    """
    return text[::-1]

