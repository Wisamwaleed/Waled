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

st.set_page_config(page_title="Waled Autonomous Developer", page_icon="🤖")

st.title("🤖 Waled Autonomous Developer Agent")
st.write("وكيل مطور حقيقي: يمتلك صلاحيات قراءة وتعديل الملفات، البحث، الذاكرة، وتنفيذ الأكواد.")

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
    tools.list_files
]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("اطلب من المطور أي مهمة برمجية (مثلاً: استعرض ملفات المشروع أو عدل كذا...)")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("جاري تشغيل الوكيل وتطبيق أدوات التطوير...")

        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=agent_tools,
                    system_instruction=(
                        "أنت مطور ووكيل برمجيات حقيقي ومستقل (Autonomous Developer Agent). "
                        "تمتلك القدرة الكاملة على قراءة ملفات المشروع، تعديلها، كتابة أكواد جديدة، اختبارها عبر تنفيذها، "
                        "والبحث في الويب والذاكرة المستقرة. عندما يطلب منك المستخدم تطوير ميزة أو إصلاح خطأ، "
                        "استخدم أدوات المطور (read_project_file, write_project_file, list_files) للتعامل مع الشيفرة البرمجية مباشرة."
                    )
                )
            )
            
            reply_text = response.text if response.text else "تم تنفيذ المهمة البرمجية بنجاح."
            message_placeholder.markdown(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            
        except Exception as e:
            message_placeholder.markdown(f"حدث خطأ أثناء عمل الوكيل: {e}")