import os
import streamlit as st
from google import genai

# إعداد مفتاح API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

st.set_page_config(page_title="Waled AI Agent", page_icon="🤖")

st.title("🤖 My Autonomous AI Agent")
st.write("مرحباً بك! وكيلك الذكي جاهز للإجابة على أسئلتك.")

if not api_key:
    st.error("الرجاء إعداد مفتاح GEMINI_API_KEY في إعدادات المنصة السحابية (Secrets).")
    st.stop()

client = genai.Client(api_key=api_key)

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
        message_placeholder.markdown("جاري التفكير...")

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            reply_text = response.text
            message_placeholder.markdown(reply_text)
            st.session_state.messages.append({"role": "assistant", "content": reply_text})
            
        except Exception as e:
            message_placeholder.markdown(f"حدث خطأ أثناء التشغيل: {e}")