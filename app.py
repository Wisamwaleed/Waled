import os
import streamlit as st
from google import genai
from google.genai import types
from groq import Groq
import tools

st.set_page_config(page_title="Waled Autonomous Developer", page_icon="🤖")

st.title("🤖 Waled Self-Evolving Developer Agent")
st.write("وكيل مطور ذاتياً: يدعم أدوات التطوير، الذاكرة، وفحص الأخطاء.")

# --- إدارة المفاتيح من الشريط الجانبي أو البيئة ---
with st.sidebar:
    st.header("🔑 إعدادات المفاتيح")
    
    # مفتاح جيميني
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        try:
            gemini_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            gemini_key = ""
            
    input_gemini = st.text_input("Gemini API Key", value=gemini_key, type="password")
    
    # مفتاح Groq الجديد
    groq_key = os.environ.get("GROQ_API_KEY")
    if not groq_key:
        try:
            groq_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            groq_key = ""
            
    input_groq = st.text_input("Groq API Key (اختياري للسرعة)", value=groq_key, type="password")
    
    # اختيار النموذج الأساسي
    provider = st.radio("اختر المزود (Provider):", ["Gemini (Google)", "Groq (Llama 3)"])

# التحقق من توفر المفتاح المختار
if provider == "Gemini (Google)" and not input_gemini:
    st.error("الرجاء إدخال مفتاح Gemini API Key للبدء.")
    st.stop()
elif provider == "Groq (Llama 3)" and not input_groq:
    st.error("الرجاء إدخال مفتاح Groq API Key للبدء.")
    st.stop()

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
                client = genai.Client(api_key=input_gemini)
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
                
            else:
                # تشغيل نموذج Groq فائق السرعة
                client = Groq(api_key=input_groq)
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", # نموذج قوي وسريع يدعم المهام المعقدة
                    messages=[
                        {
                            "role": "system",
                            "content": "أنت مساعد ومطور ذكي ومستقل لمشروع برمجيات بايثون."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=2048,
                )
                reply_text = completion.choices[0].message.content

            message_placeholder.markdown(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            
        except Exception as e:
            message_placeholder.markdown(f"حدث خطأ أثناء التشغيل: {e}")