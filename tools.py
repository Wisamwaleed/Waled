import os
import subprocess
import urllib.request
import urllib.parse
from html.parser import HTMLParser
import memory_manager
import dev_tools
import self_debug_tool

# الأدوات الأساسية والأدوات السابقة...
def web_search(query: str) -> str:
    """البحث في الإنترنت عن معلومات حية."""
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            html_content = resp.read().decode('utf-8')
            
            class HTMLFilter(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []
                def handle_data(self, data):
                    self.text.append(data)
            
            parser = HTMLFilter()
            parser.feed(html_content)
            results = " ".join([t.strip() for t in parser.text if t.strip()])
            return results[:1500] if results else "لم يتم العثور على نتائج."
    except Exception as e:
        return f"خطأ في البحث: {e}"

def run_python_code(code: str) -> str:
    """تنفيذ كود بايثون محلياً واختباره."""
    try:
        filename = "temp_exec.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        res = subprocess.run(["python", filename], capture_output=True, text=True, timeout=10)
        output = res.stdout if res.returncode == 0 else res.stderr
        return output if output else "تم التنفيذ بنجاح دون مخرجات."
    except Exception as e:
        return f"خطأ أثناء التنفيذ: {e}"

def store_lesson(category: str, content: str) -> str:
    """حفظ ملاحظة أو درس في الذاكرة المستقرة."""
    return memory_manager.save_memory(category, content)

def query_memory(query: str) -> str:
    """البحث في الذاكرة المستقرة عن معلومات سابقة."""
    return memory_manager.search_memory(query)

def read_project_file(file_path: str) -> str:
    """قراءة ملف برمجي داخل المشروع."""
    return dev_tools.read_file(file_path)

def write_project_file(file_path: str, content: str) -> str:
    """كتابة أو تعديل ملف برمجي داخل المشروع."""
    return dev_tools.write_file(file_path, content)

def list_files() -> str:
    """عرض ملفات المشروع الحالية."""
    return dev_tools.list_workspace_files()

# أداة التطوير الذاتي الجديدة
def check_code_syntax(file_path: str) -> str:
    """فحص سلامة وصحة الكود البرمجي في أي ملف واكتشاف الأخطاء."""
    return self_debug_tool.test_and_fix_file(file_path)