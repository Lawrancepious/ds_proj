import plotly.express as px
import streamlit as st

from core import ai, ui
from core.data import IRIS_COLORS, IRIS_FEATURES, load_iris

ai.sidebar_settings()
df = load_iris()

ui.hero("Iris dashboard", "150 iris flowers from three species, each measured on four "
        "features in centimetres.", "🌸", ["150 flowers", "3 species", "4 features"])

species = st.multiselect("Species", list(IRIS_COLORS), default=list(IRIS_COLORS))
view = df[df["Species"].isin(species)]
if view.empty:
    st.info("Select at least one species.")
    st.stop()

# --- headline numbers -------------------------------------------------------
cols = st.columns(4)
for col, feat in zip(cols, IRIS_FEATURES):
    col.metric(f"Mean {feat.replace('Cm', '')}", f"{view[feat].mean():.2f} cm",
               f"σ {view[feat].std():.2f}", delta_color="off")

tab_dist, tab_rel, tab_stats = st.tabs(["Distributions", "Relationships", "Statistics"])

with tab_dist:
    feat = st.selectbox("Feature", IRIS_FEATURES, index=2)
    c1, c2 = st.columns(2)
    c1.plotly_chart(
        px.histogram(view, x=feat, color="Species", color_discrete_map=IRIS_COLORS,
                     barmode="overlay", opacity=0.7, nbins=25, title=f"Histogram of {feat}"),
        use_container_width=True)
    c2.plotly_chart(
        px.box(view, x="Species", y=feat, color="Species", color_discrete_map=IRIS_COLORS,
               points="all", title=f"{feat} by species"),
        use_container_width=True)
    st.plotly_chart(
        px.violin(view.melt(id_vars="Species", value_vars=IRIS_FEATURES),
                  x="variable", y="value", color="Species", color_discrete_map=IRIS_COLORS,
                  box=True, title="All four features side by side",
                  labels={"variable": "", "value": "cm"}),
        use_container_width=True)

with tab_rel:
    c1, c2 = st.columns(2)
    x = c1.selectbox("X axis", IRIS_FEATURES, index=2)
    y = c2.selectbox("Y axis", IRIS_FEATURES, index=3)
    st.plotly_chart(
        px.scatter(view, x=x, y=y, color="Species", color_discrete_map=IRIS_COLORS,
                   marginal_x="histogram", marginal_y="histogram", title=f"{y} vs {x}"),
        use_container_width=True)
    st.plotly_chart(
        px.scatter_matrix(view, dimensions=IRIS_FEATURES, color="Species",
                          color_discrete_map=IRIS_COLORS, height=650,
                          title="Scatter matrix - every pair of features"),
        use_container_width=True)
    corr = view[IRIS_FEATURES].corr().round(2)
    st.plotly_chart(
        px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                  title="Correlation between features"),
        use_container_width=True)

with tab_stats:
    st.subheader("Summary by species")
    st.dataframe(view.groupby("Species")[IRIS_FEATURES].agg(["mean", "std", "min", "max"]).round(2))
    st.subheader("Raw data")
    st.dataframe(view, hide_index=True, height=300)
    st.download_button("Download filtered CSV", view.to_csv(index=False), "iris_filtered.csv",
                       icon=":material/download:")

st.divider()
st.subheader("AI insights")
summary = view.groupby("Species")[IRIS_FEATURES].describe().round(2).to_string()
ai.insight_button(
    "Explain what this data shows",
    "Give 4-6 key insights about these iris species: which features separate them best, "
    "which species overlap, and what a botanist or ML engineer should take away. "
    f"Species currently selected: {', '.join(species)}.",
    f"Per-species summary statistics:\n{summary}\n\nCorrelations:\n{corr.to_string()}",
    key="iris_insight",
)

ui.footer()
