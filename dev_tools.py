import os

def read_file(file_path: str) -> str:
    """قراءة محتوى أي ملف برمجي أو نصي في المشروع."""
    try:
        if not os.path.exists(file_path):
            return f"خطأ: الملف {file_path} غير موجود."
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"خطأ أثناء قراءة الملف: {e}"

def write_file(file_path: str, content: str) -> str:
    """إنشاء ملف جديد أو تعديل ملف موجود وكتابة الكود فيه."""
    try:
        dir_name = os.path.dirname(file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"تم حفظ وتحديث الملف {file_path} بنجاح."
    except Exception as e:
        return f"خطأ أثناء كتابة الملف: {e}"

def list_workspace_files() -> str:
    """استعراض جميع ملفات ومجلدات المشروع لمعرفة الهيكلية البرمجية."""
    try:
        file_list = []
        for root, dirs, files in os.walk("."):
            # استبعاد المجلدات غير الضرورية
            dirs[:] = [d for d in dirs if d not in ['.git', 'venv', '__pycache__', 'memory']]
            for file in files:
                file_list.append(os.path.join(root, file))
        return "\n".join(file_list) if file_list else "لا توجد ملفات."
    except Exception as e:
        return f"خطأ في استعراض المجلدات: {e}"