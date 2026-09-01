import os
import subprocess
import json
import urllib.request
import urllib.parse

def web_search(query: str) -> str:
    """البحث في الإنترنت عن طريق جلب نتائج بحث بسيطة أو معلومات عامة."""
    try:
        # استخدام واجهة بحث عامة أو محاكاة البحث
        encoded_query = urllib.parse.quote(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
            # استخراج بعض النصوص المبسطة من نتائج البحث
            from html.parser import HTMLParser
            
            class HTMLFilter(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []
                def handle_data(self, data):
                    self.text.append(data)
            
            parser = HTMLFilter()
            parser.feed(html_content)
            results = " ".join([t.strip() for t in parser.text if t.strip()])
            return results[:2000] if results500 else "لم يتم العثور على نتائج واضحة."
    except Exception as e:
        return f"خطأ في البحث: {e}"

def run_python_code(code: str) -> str:
    """تنفيذ كود بايثون محلياً وإرجاع النتيجة أو الأخطاء لتصحيحها ذاتياً."""
    try:
        # كتابة الكود في ملف مؤقت وتنفيذه
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
        return output if output else "تم تنفيذ الكود بنجاح دون مخرجات نصية."
    except Exception as e:
        return fعبارة عن خطأ أثناء التنفيذ: {e}"

def save_memory(memory_text: str) -> str:
    """حفظ التجارب أو الدروس المستفادة في ملف ذاكرة خاص ليتطور الوكيل ذاتياً."""
    try:
        os.makedirs("memory", exist_ok=True)
        with open("memory/learned_lessons.txt", "a", encoding="utf-8") as f:
            f.write(f"- {memory_text}\n")
        return "تم حفظ التعلم بنجاح في الذاكرة الدائمة."
    except Exception as e:
        return f"خطأ في حفظ الذاكرة: {e}"

def read_memory() -> str:
    """قراءة الذاكرة والتجارب السابقة للرجوع إليها عند الحاجة."""
    try:
        if os.path.exists("memory/learned_lessons.txt"):
            with open("memory/learned_lessons.txt", "r", encoding="utf-8") as f:
                return f.read()
        return "الذاكرة فارغة حتى الآن."
    except Exception as e:
        return f"خطأ في قراءة الذاكرة: {e}"