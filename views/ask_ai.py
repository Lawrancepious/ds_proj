import streamlit as st

from core import ai, ui
from core.data import dataset_context

ai.sidebar_settings()

ui.hero("Ask your data", "Chat with Google Gemini. The whole dataset is sent along with "
        "your question, so answers are grounded in the actual rows.", "💬",
        ["Gemini", "streaming answers"])

dataset = st.segmented_control("Dataset", ["Iris", "Titanic"], default="Iris")
if dataset is None:
    st.stop()

SUGGESTIONS = {
    "Iris": ["Which single feature best separates the three species?",
             "Write a one-paragraph summary of this dataset for a report.",
             "Are there any outliers? List them with their Id."],
    "Titanic": ["How does the average fare differ between classes and ports?",
                "What share of children travelled in 3rd class?",
                "Which columns have missing values, and how would you impute them?"],
}

history_key = f"chat_{dataset}"
history = st.session_state.setdefault(history_key, [])

if not ai.get_api_key():
    st.warning("Add a Gemini API key in the sidebar to start chatting.")

for msg in history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = None
if not history:
    st.write("Try one of these:")
    for i, s in enumerate(SUGGESTIONS[dataset]):
        if st.button(s, key=f"sugg_{dataset}_{i}", icon=":material/lightbulb:"):
            question = s

question = st.chat_input(f"Ask something about the {dataset} data...") or question

if question:
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            answer = st.write_stream(ai.ask_stream(question, dataset_context(dataset), history))
        except Exception as e:
            answer = f":red[{e}]"
            st.markdown(answer)
    history += [{"role": "user", "content": question}, {"role": "assistant", "content": answer}]

if history and st.sidebar.button("Clear chat", icon=":material/delete:"):
    st.session_state[history_key] = []
    st.rerun()

ui.footer()
