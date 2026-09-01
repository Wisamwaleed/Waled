import os
import streamlit as st
from google import genai
from google.genai import types
from groq import Groq
from openai import OpenAI
import tools

st.set_page_config(page_title="Waled Autonomous Developer", page_icon="🤖")

st.title("🤖 Waled Self-Evolving Developer Agent")
st.write("وكيل مطور ذاتياً: يدعم أدوات التطوير، الذاكرة، وفحص الأخطاء مع التبديل بين Gemini، Groq، و OpenAI.")

# قراءة المفاتيح من متغيرات البيئة أو الـ Secrets
gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
groq_key = os.environ.get("GROQ_API_KEY", "").strip()
openai_key = os.environ.get("OPENAI_API_KEY", "").strip()

if not gemini_key:
    try:
        gemini_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

if not groq_key:
    try:
        groq_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        pass

if not openai_key:
    try:
        openai_key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        pass

with st.sidebar:
    st.header("🔑 إعدادات المزود والمفاتيح")
    provider = st.radio("اختر نموذج الذكاء الاصطناعي:", ["Groq (Llama 3)", "OpenAI (GPT-4o)", "Gemini (Google)"])
    
    st.markdown("---")
    if provider == "Groq (Llama 3)" and not groq_key:
        groq_key = st.text_input("أدخل مفتاح Groq API Key:", type="password")
    elif provider == "OpenAI (GPT-4o)" and not openai_key:
        openai_key = st.text_input("أدخل مفتاح OpenAI API Key:", type="password")
    elif provider == "Gemini (Google)" and not gemini_key:
        gemini_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password")

agent_tools = [
    tools.web_search,
    tools.run_python_code,
    tools.store_lesson,
    tools.query_memory,
    tools.read_project_file,
    tools.write_project_file,
    tools.list_files,
    tools.check_code_syntax
]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("اطلب من المطور الذاتي تطوير ملف أو فحص الأخطاء...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("جاري معالجة الطلب...")

        try:
            if provider == "Gemini (Google)":
                if not gemini_key:
                    raise ValueError("مفتاح Gemini غير متوفر.")
                
                client = genai.Client(api_key=gemini_key)
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        tools=agent_tools,
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(
                            disable=False,
                            maximum_remote_calls=3
                        ),
                        system_instruction=(
                            "أنت وكيل ومطور برمجيات ذاتي التطور (Self-Evolving Developer Agent). "
                            "تمتلك أدوات لقراءة ملفات المشروع، تعديلها، اختبارها، وفحص أخطائها عبر (check_code_syntax)."
                        )
                    )
                )
                reply_text = response.text if response.text else "تم تنفيذ مهام التطوير بنجاح."
                
            elif provider == "Groq (Llama 3)":
                if not groq_key:
                    raise ValueError("مفتاح Groq غير متوفر.")
                
                client = Groq(api_key=groq_key)
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "أنت مساعد ومطور ذكي ومستقل لمشروع برمجيات بايثون."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2048,
                )
                reply_text = completion.choices[0].message.content

            else:  # OpenAI
                if not openai_key:
                    raise ValueError("مفتاح OpenAI غير متوفر.")
                
                client = OpenAI(api_key=openai_key)
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",  # نموذج سريع واقتصادي وعالي الكفاءة
                    messages=[
                        {"role": "system", "content": "أنت مساعد ومطور ذكي ومستقل لمشروع برمجيات بايثون."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2048,
                )
                reply_text = completion.choices[0].message.content

            message_placeholder.markdown(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            
        except Exception as e:
            message_placeholder.markdown(f"حدث خطأ أثناء التشغيل: {e}")
