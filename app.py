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

st.title("🤖 Waled Autonomous Agent")
st.write("وكيل حقيقي يمتلك أدوات البحث، تنفيذ الأكواد، والذاكرة الذاتية.")

if not api_key:
    st.error("الرجاء إعداد مفتاح GEMINI_API_KEY في إعدادات المنصة السحابية.")
    st.stop()

client = genai.Client(api_key=api_key)

# قائمة الأدوات المتاحة للوكيل
agent_tools = [
    tools.web_search,
    tools.run_python_code,
    tools.save_memory,
    tools.read_memory
]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("اطلب من الوكيل تنفيذ مهمة (مثلاً: ابحث عن... أو اكتب كود بايثون لاختبار...)")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("جاري تشغيل الوكيل وتجربة الأدوات...")

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=agent_tools,
                    system_instruction=(
                        "أنت وكيل ذكي ومستقل (Autonomous Agent). "
                        "لديك أدوات للبحث في الويب، تشغيل أكواد بايثون، وحفظ أو قراءة الذاكرة. "
                        "استخدم هذه الأدوات عندما يطلب منك المستخدم مهام تتطلب ذلك."
                    )
                )
            )
            
            reply_text = response.text if response.text else "تم تنفيذ المهمة بنجاح عبر الأدوات."
            message_placeholder.markdown(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            
        except Exception as e:
            message_placeholder.markdown(f"حدث خطأ أثناء عمل الوكيل: {e}")