import os
import sqlite3
import json

DB_FILE = "memory/agent_memory.db"

def init_memory():
    """إنشاء جدول الذاكرة إذا لم يكن موجوداً."""
    os.makedirs("memory", exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS long_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_memory(category: str, content: str) -> str:
    """حفظ معلومة أو درس جديد في الذاكرة المستقرة."""
    try:
        init_memory()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO long_term_memory (category, content) VALUES (?, ?)", (category, content))
        conn.commit()
        conn.close()
        return "تم حفظ المعلومة بنجاح في قاعدة بيانات الذاكرة المستقرة."
    except Exception as e:
        return f"خطأ في حفظ الذاكرة: {e}"

def search_memory(query: str) -> str:
    """البحث واسترجاع المعلومات السابقة من الذاكرة المستقرة."""
    try:
        init_memory()
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT category, content, timestamp FROM long_term_memory WHERE content LIKE ? OR category LIKE ?", 
                       (f"%{query}%", f"%{query}%"))
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return "لا توجد نتائج مطابقة في الذاكرة."
        
        results = []
        for row in rows:
            results.append(f"[{row[2]}] ({row[0]}): {row[1]}")
        return "\n".join(results)
    except Exception as e:
        return f"خطأ في قراءة الذاكرة: {e}"