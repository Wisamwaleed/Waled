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

st.title("🤖 Waled Autonomous Agent (ReAct Loop)")
st.write("وكيل ذكي حقيقي قادر على تنفيذ سلاسل مهام متعددة الخطوات تلقائياً.")

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

prompt = st.chat_input("اطرح طلباً معقداً يتطلب خطوات متعددة (مثلاً: استعرض الملفات، اقرأ ملف معين، واقترح تعديلات)...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("جاري تشغيل حلقة التفكير والتنفيذ المستقلة (ReAct)...")

        try:
            # تفعيل الاستدعاء التلقائي المتعدد للأدوات (Automatic Function Calling)
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=agent_tools,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=False,
                        maximum_remote_calls=5  # السماح للوكيل بما يصل إلى 5 خطوات متتالية لحل المشكلة
                    ),
                    system_instruction=(
                        "أنت وكيل ذكي ومستقل (Autonomous Developer Agent). "
                        "تمتلك القدرة على قراءة ملفات المشروع، تعديلها، كتابة أكواد واختبارها، والبحث في الويب والذاكرة. "
                        "عندما يطلب منك المستخدم مهمة، قم بتفكيكها إلى خطوات واستخدم الأدوات بشكل متتابع (أداة تلو الأخرى) "
                        "حتى تصل إلى النتيجة النهائية وتنجز المهمة بالكامل قبل الرد النهائي على المستخدم."
                    )
                )
            )
            
            reply_text = response.text if response.text else "تم إتمام المهمة بنجاح عبر حلقة التنفيذ."
            message_placeholder.markdown(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            
        except Exception as e:
            message_placeholder.markdown(f"حدث خطأ أثناء تنفيذ الوكيل: {e}")