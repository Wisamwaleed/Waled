import os
import streamlit as st
from google import genai
from google.genai import types
import tools

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

st.set_page_config(page_title="Waled Self-Evolving Developer", page_icon="🤖")

st.title("🤖 Waled Self-Evolving Developer Agent")
st.write("وكيل مطور ذاتياً: يستعرض، يكتب، يفحص الأخطاء البرمجية ويصلحها بذكاء.")

if not api_key:
    st.error("الرجاء إعداد مفتاح GEMINI_API_KEY في إعدادات المنصة.")
    st.stop()

client = genai.Client(api_key=api_key)

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
        message_placeholder.markdown("جاري معالجة طلب التطوير الذاتي...")

        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=agent_tools,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=False,
                        maximum_remote_calls=3  # حد آمن واقتصادي لا يستهلك حصة الطلبات اليومية
                    ),
                    system_instruction=(
                        "أنت وكيل ومطور برمجيات ذاتي التطور (Self-Evolving Developer Agent). "
                        "تمتلك أدوات لقراءة ملفات المشروع، تعديلها، اختبارها، وفحص أخطائها عبر (check_code_syntax). "
                        "عندما يطلب منك المستخدم تطوير ميزة أو فحص ملف، استخدم هذه الأدوات بحكمة واقتصاد."
                    )
                )
            )
            
            reply_text = response.text if response.text else "تم تنفيذ مهام التطوير بنجاح."
            message_placeholder.markdown(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            
        except Exception as e:
            message_placeholder.markdown(f"حدث خطأ أثناء تشغيل الوكيل: {e}")