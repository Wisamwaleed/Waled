import os
import streamlit as st
from google import genai
from google.genai import types
import tools

# إعداد مفتاح API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

st.set_page_config(page_title="Waled AI Agent", page_icon="🤖")

st.title("🤖 My Autonomous AI Agent")
st.write("وكيلك الذكي المتصل دائماً والمتاح للعمل مع ميزات البحث والذاكرة والتطور الذاتي.")

if not api_key:
    st.error("الرجاء إعداد مفتاح GEMINI_API_KEY في إعدادات المنصة السحابية أو محلياً.")
    st.stop()

client = genai.Client(api_key=api_key)

# تعريف الأدوات المتاحة للوكيل
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

if prompt := st.chat_input("اكتب طلبك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("جاري التفكير والتنفيذ...")

        try:
            # استدعاء نموذج جيميني مع تفعيل الأدوات والذاكرة
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    tools=agent_tools,
                    system_instruction="أنت 'وِسام'، وكيل ذكي ومطور ذاتياً. تستطيع البحث في الويب، تنفيذ أكواد بايثون، وحفظ الدروس في الذاكرة لتتطور باستمرار."
                )
            )
            
            reply_text = response.text if response.text else "تم تنفيذ الطلب بنجاح."
            message_placeholder.markdown(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            
        except Exception as e:
            error_msg = f"حدث خطأ أثناء التشغيل: {e}"
            message_placeholder.markdown(error_msg)