import os
import subprocess
import urllib.request
import urllib.parse

def web_search(query: str) -> str:
    """البحث في الإنترنت باستخدام DuckDuckGo."""
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            return html[:1500] if html else "لم يتم العثور على نتائج."
    except Exception as e:
        return f"حدث خطأ أثناء البحث: {str(e)}"

def run_python_code(code: str) -> str:
    """تنفيذ كود بايثون محلياً وإرجاع النتيجة."""
    try:
        filename = "temp_exec.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        
        result = subprocess.run(
            ["python", filename], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        output = result.stdout if result.returncode == 0 else result.stderr
        return output if output else "تم التنفيذ بنجاح دون مخرجات."
    except Exception as e:
        return f"حدث خطأ أثناء تنفيذ الكود: {str(e)}"

def save_memory(memory_text: str) -> str:
    """حفظ الدروس والمعلومات في الذاكرة المستمرة."""
    try:
        os.makedirs("memory", exist_ok=True)
        file_path = os.path.join("memory", "learned_lessons.txt")
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"- {memory_text}\n")
        return "تم حفظ المعلومة في الذاكرة بنجاح."
    except Exception as e:
        return f"حدث خطأ أثناء حفظ الذاكرة: {str(e)}"

def read_memory() -> str:
    """قراءة محتوى الذاكرة السابقة."""
    try:
        file_path = os.path.join("memory", "learned_lessons.txt")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        return "الذاكرة فارغة حالياً."
    except Exception as e:
        return f"حدث خطأ أثناء قراءة الذاكرة: {str(e)}"