import subprocess
import os

def test_and_fix_file(file_path: str) -> str:
    """تشغيل وفحص أي ملف بايثون في المشروع لاكتشاف الأخطاء البرمجية وإصلاحها."""
    try:
        if not os.path.exists(file_path):
            return f"خطأ: الملف {file_path} غير موجود."
            
        # تشغيل فحص السنتكس والتشغيل
        result = subprocess.run(["python", "-m", "py_compile", file_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            return f"الملف {file_path} سليم ولا يوجد فيه أي أخطاء برمجية."
        else:
            error_msg = result.stderr
            return f"تم اكتشاف خطأ في الملف {file_path}:\n{error_msg}\nالرجاء استخدام أداة write_project_file لتعديل الكود وإصلاح هذا الخطأ."
    except Exception as e:
        return f"حدث خطأ أثناء فحص الملف: {e}"