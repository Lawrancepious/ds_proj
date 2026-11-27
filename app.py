import streamlit as st

from core import ui

st.set_page_config(page_title="DS Project - Iris & Titanic", page_icon=":bar_chart:",
                   layout="wide")

pages = {
    "Home": [st.Page("views/home.py", title="Overview", icon=":material/home:", default=True)],
    "Dashboards": [
        st.Page("views/iris_dashboard.py", title="Iris dashboard", icon=":material/local_florist:"),
        st.Page("views/titanic_dashboard.py", title="Titanic dashboard", icon=":material/directions_boat:"),
    ],
    "Machine learning": [
        st.Page("views/iris_classifier.py", title="Iris classifier", icon=":material/model_training:"),
    ],
    "AI": [
        st.Page("views/ask_ai.py", title="Ask your data", icon=":material/chat:"),
    ],
}

nav = st.navigation(pages)
ui.setup()
nav.run()
