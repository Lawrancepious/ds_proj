import plotly.express as px
import streamlit as st

from core import ai, ui
from core.data import load_titanic

ai.sidebar_settings()
df = load_titanic()

ui.hero("Titanic dashboard", "418 passengers from the Kaggle Titanic test split: who they "
        "were, what they paid, and who they travelled with.", "🚢",
        ["418 passengers", "3 classes", "3 ports"])

if not st.session_state.get("titanic_snow"):   # a little North Atlantic weather
    st.session_state.titanic_snow = True
    st.snow()

# --- filters ------------------------------------------------------------------
with st.sidebar:
    st.subheader("Filters")
    port_options = sorted(df["Port"].unique())
    sexes = st.pills("Sex", ["male", "female"], selection_mode="multi", default=["male", "female"])
    classes = st.pills("Class", ["1st", "2nd", "3rd"], selection_mode="multi",
                       default=["1st", "2nd", "3rd"])
    ports = st.pills("Port of embarkation", port_options, selection_mode="multi",
                     default=port_options)

view = df[df["Sex"].isin(sexes) & df["Class"].isin(classes) & df["Port"].isin(ports)]
if view.empty:
    st.info("No passengers match these filters.")
    st.stop()

c = st.columns(5)
c[0].metric("Passengers", len(view))
c[1].metric("Women", f"{(view['Sex'] == 'female').mean():.0%}")
c[2].metric("Median age", f"{view['Age'].median():.0f}")
c[3].metric("Median fare", f"£{view['Fare'].median():.2f}")
c[4].metric("Travelling alone", f"{(view['FamilySize'] == 1).mean():.0%}")

CLASS_ORDER = {"Class": ["1st", "2nd", "3rd"]}
tab_who, tab_money, tab_family, tab_baseline, tab_data = st.tabs(
    ["Who was on board", "Fares & class", "Families", "Baseline model", "Data"])

with tab_who:
    c1, c2 = st.columns(2)
    c1.plotly_chart(
        px.histogram(view, x="Age", color="Sex", nbins=30, barmode="overlay", opacity=0.7,
                     title="Age distribution by sex"),
        use_container_width=True)
    c2.plotly_chart(
        px.sunburst(view, path=["Class", "Sex"], title="Class → sex (click a slice to zoom)"),
        use_container_width=True)
    c1.plotly_chart(
        px.histogram(view, x="Title", color="Class", category_orders=CLASS_ORDER,
                     title="Passenger titles (extracted from names)"),
        use_container_width=True)
    c2.plotly_chart(
        px.pie(view, names="Port", hole=0.45, title="Port of embarkation"),
        use_container_width=True)

with tab_money:
    c1, c2 = st.columns(2)
    c1.plotly_chart(
        px.box(view, x="Class", y="Fare", color="Class", category_orders=CLASS_ORDER,
               points="outliers", log_y=True, title="Fare by class (log scale)"),
        use_container_width=True)
    c2.plotly_chart(
        px.scatter(view, x="Age", y="Fare", color="Class", category_orders=CLASS_ORDER,
                   hover_name="Name", log_y=True, title="Age vs fare"),
        use_container_width=True)
    st.plotly_chart(
        px.histogram(view, x="Port", color="Class", barmode="group", category_orders=CLASS_ORDER,
                     title="Class mix at each port"),
        use_container_width=True)
    known = view[view["Deck"] != "Unknown"]
    st.caption(f"Cabin deck is only known for {len(known)} of {len(view)} passengers "
               f"({len(known) / len(view):.0%}), almost all of them 1st class.")

with tab_family:
    c1, c2 = st.columns(2)
    c1.plotly_chart(
        px.histogram(view, x="FamilySize", color="Class", category_orders=CLASS_ORDER,
                     title="Family size on board (incl. passenger)"),
        use_container_width=True)
    c2.plotly_chart(
        px.histogram(view, x="Class", color="TravelType", barnorm="percent",
                     category_orders=CLASS_ORDER, title="Travelling alone vs with family (%)"),
        use_container_width=True)

with tab_baseline:
    st.warning(
        "This file has **no real survival labels**. `gender_submission.csv` is Kaggle's sample "
        "submission: a naive baseline that predicts *every woman survived and every man died*. "
        "It scores about 76.6% on Kaggle's hidden labels, which is the bar any real model has "
        "to beat."
    )
    st.plotly_chart(
        px.histogram(view, x="Class", color=view["BaselinePrediction"].map(
            {1: "Predicted survived", 0: "Predicted died"}), category_orders=CLASS_ORDER,
            barmode="group", title="What the baseline predicts, by class",
            labels={"color": ""}),
        use_container_width=True)

with tab_data:
    st.dataframe(view.drop(columns=["Pclass", "Embarked"]), hide_index=True, height=400)
    st.download_button("Download filtered CSV", view.to_csv(index=False), "titanic_filtered.csv",
                       icon=":material/download:")

st.divider()
st.subheader("AI insights")
cols = ["Sex", "Class", "Port", "AgeGroup", "Title", "TravelType"]
counts = "\n\n".join(view[c].value_counts().to_string() for c in cols)
ai.insight_button(
    "Tell me the story of these passengers",
    "Describe this group of Titanic passengers in 5-7 bullet points: demographics, wealth "
    "(class & fare), family structure and anything surprising. Remember there are no real "
    "survival labels here, so do not claim who survived.",
    f"Filtered passengers: {len(view)}\n\nNumeric summary:\n"
    f"{view[['Age', 'Fare', 'FamilySize']].describe().round(2).to_string()}\n\n"
    f"Fare by class:\n{view.groupby('Class')['Fare'].describe().round(2).to_string()}\n\n"
    f"Category counts:\n{counts}",
    key="titanic_insight",
)

ui.footer()
