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

st.set_page_config(page_title="Waled Autonomous Agent", page_icon="🤖")

st.title("🤖 Waled Autonomous Agent (مع الذاكرة المستقرة)")
st.write("وكيل مزود بأدوات بحث، تشغيل كود، وذاكرة مستقرة تعتمد على قواعد البيانات.")

if not api_key:
    st.error("الرجاء إعداد مفتاح GEMINI_API_KEY في إعدادات المنصة.")
    st.stop()

client = genai.Client(api_key=api_key)

agent_tools = [
    tools.web_search,
    tools.run_python_code,
    tools.store_lesson,
    tools.query_memory
]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("اطرح طلباً أو اطلب منه حفظ معلومة في الذاكرة...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("جاري معالجة الطلب واستخدام الذاكرة أو الأدوات...")

        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=agent_tools,
                    system_instruction=(
                        "أنت وكيل ذكي ومستقل (Autonomous Agent) تمتلك ذاكرة مستقرة، وأدوات بحث وتنفذ أكواد. "
                        "عندما يطلب منك المستخدم حفظ معلومة، استخدم أداة store_lesson. "
                        "وعندما يسأل عن معلومة قديمة، استخدم أداة query_memory."
                    )
                )
            )
            
            reply_text = response.text if response.text else "تم تنفيذ العملية بنجاح."
            message_placeholder.markdown(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            
        except Exception as e:
            message_placeholder.markdown(f"حدث خطأ: {e}")