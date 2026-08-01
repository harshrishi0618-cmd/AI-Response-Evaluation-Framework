import streamlit as st

st.set_page_config(
    page_title="AI Response Evaluation Framework",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI Response Evaluation Framework")
st.markdown("Evaluate AI-generated responses using multiple quality metrics.")

prompt = st.text_area(
    "Prompt",
    height=150,
    placeholder="Enter the user's prompt...",
)

response = st.text_area(
    "AI Response",
    height=250,
    placeholder="Enter the AI response...",
)

if st.button("Evaluate"):
    if not prompt.strip() or not response.strip():
        st.error("Please enter both a prompt and a response.")
    else:
        st.success("Dashboard is connected successfully! 🎉")
        st.info("Next step: connect the Evaluation Engine.")
