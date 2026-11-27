import streamlit as st

from core import ui
from core.data import RESOURCES, load_iris, load_titanic

ui.hero("Data Science Project",
        "Interactive exploration of two classic datasets, a live machine-learning model "
        "and a Gemini-powered assistant that answers questions about the data.",
        "📊", ["Streamlit", "scikit-learn", "Plotly", "Google Gemini"])

if not st.session_state.get("welcomed"):
    st.session_state.welcomed = True
    st.balloons()
    st.toast("Welcome! Pick a page from the sidebar.", icon=":material/waving_hand:")

iris, titanic = load_iris(), load_titanic()

col1, col2 = st.columns(2)
with col1, st.container(border=True):
    st.image(str(RESOURCES / "iris.jpg"))
    st.subheader("Iris flowers")
    a, b, c = st.columns(3)
    a.metric("Flowers", len(iris))
    b.metric("Species", iris["Species"].nunique())
    c.metric("Features", 4)
    st.page_link("views/iris_dashboard.py", label="Open dashboard", icon=":material/arrow_forward:")
    st.page_link("views/iris_classifier.py", label="Train a classifier", icon=":material/arrow_forward:")

with col2, st.container(border=True):
    st.image(str(RESOURCES / "titanic.jpg"))
    st.subheader("Titanic passengers")
    a, b, c = st.columns(3)
    a.metric("Passengers", len(titanic))
    b.metric("Women", f"{(titanic['Sex'] == 'female').mean():.0%}")
    c.metric("Median fare", f"£{titanic['Fare'].median():.0f}")
    st.page_link("views/titanic_dashboard.py", label="Open dashboard", icon=":material/arrow_forward:")

with st.container(border=True):
    st.markdown("#### :red[:material/auto_awesome:] Ask Gemini anything")
    st.caption("Chat with an AI that has read every row of both datasets.")
    st.page_link("views/ask_ai.py", label="Start chatting", icon=":material/arrow_forward:")

ui.footer()
