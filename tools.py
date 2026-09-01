import os
import subprocess
import urllib.request
import urllib.parse
from html.parser import HTMLParser

def web_search(query: str) -> str:
    """Search the web for real-time information or general knowledge."""
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
    """Execute Python code locally and return the output or errors for self-correction."""
    try:
        filename = "temp_exec.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        res = subprocess.run(["python", filename], capture_output=True, text=True, timeout=10)
        output = res.stdout if res.returncode == 0 else res.stderr
        return output if output else "تم تنفيذ الكود بنجاح دون مخرجات."
    except Exception as e:
        return f"خطأ أثناء التنفيذ: {e}"

def save_memory(memory_text: str) -> str:
    """Save experiences, lessons, or notes into a persistent memory file."""
    try:
        os.makedirs("memory", exist_ok=True)
        with open("memory/learned_lessons.txt", "a", encoding="utf-8") as f:
            f.write(f"- {memory_text}\n")
        return "تم حفظ المعلومة في الذاكرة بنجاح."
    except Exception as e:
        return f"خطأ في حفظ الذاكرة: {e}"

def read_memory() -> str:
    """Read past memories and saved lessons to retrieve context."""
    try:
        if os.path.exists("memory/learned_lessons.txt"):
            with open("memory/learned_lessons.txt", "r", encoding="utf-8") as f:
                return f.read()
        return "الذاكرة فارغة حالياً."
    except Exception as e:
        return f"خطأ في قراءة الذاكرة: {e}"