import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from core import ai, ui
from core.data import IRIS_COLORS, IRIS_FEATURES, load_iris

ai.sidebar_settings()
df = load_iris()
X, y = df[IRIS_FEATURES], df["Species"]

MODELS = {
    "Logistic regression": lambda: make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "K-nearest neighbours": lambda: make_pipeline(StandardScaler(), KNeighborsClassifier(5)),
    "Support vector machine": lambda: make_pipeline(StandardScaler(), CalibratedClassifierCV(SVC(random_state=0))),
    "Decision tree": lambda: DecisionTreeClassifier(max_depth=3, random_state=0),
    "Random forest": lambda: RandomForestClassifier(200, random_state=0),
}

ui.hero("Iris classifier", "Train a model to predict the species from four flower "
        "measurements, then test it on a flower you design.", "🤖",
        ["5 algorithms", "cross-validation", "live predictions"])


@st.cache_data(show_spinner=False)
def compare_models() -> pd.DataFrame:
    rows = []
    for name, build in MODELS.items():
        scores = cross_val_score(build(), X, y, cv=5)
        rows.append({"Model": name, "Mean accuracy": scores.mean(), "Std": scores.std()})
    return pd.DataFrame(rows).sort_values("Mean accuracy", ascending=False)


# --- 1. compare models ------------------------------------------------------------
st.subheader("1. Compare models (5-fold cross-validation)")
with st.spinner("Training 5 models x 5 folds..."):
    scores = compare_models()
st.plotly_chart(
    px.bar(scores, x="Mean accuracy", y="Model", error_x="Std", orientation="h",
           range_x=[0.8, 1.0], text=scores["Mean accuracy"].map("{:.1%}".format)),
    use_container_width=True)

# --- 2. train one -----------------------------------------------------------------
st.subheader("2. Train and evaluate")
c1, c2 = st.columns([2, 1])
model_name = c1.selectbox("Model", list(MODELS), index=list(MODELS).index(scores.iloc[0]["Model"]))
test_size = c2.slider("Test set size", 0.1, 0.5, 0.3, 0.05)

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=test_size, stratify=y, random_state=42)
model = MODELS[model_name]().fit(X_tr, y_tr)
pred = model.predict(X_te)
acc = accuracy_score(y_te, pred)

m1, m2, m3 = st.columns(3)
m1.metric("Test accuracy", f"{acc:.1%}")
m2.metric("Training flowers", len(X_tr))
m3.metric("Misclassified", int((pred != y_te).sum()))

run_id = (model_name, test_size)
if acc == 1.0 and st.session_state.get("celebrated") != run_id:
    st.session_state.celebrated = run_id
    st.balloons()
    st.toast(f"Perfect score! {model_name} got every test flower right.", icon=":material/celebration:")

labels = list(IRIS_COLORS)
c1, c2 = st.columns(2)
c1.plotly_chart(
    px.imshow(confusion_matrix(y_te, pred, labels=labels), x=labels, y=labels, text_auto=True,
              labels={"x": "Predicted", "y": "Actual"},
              title="Confusion matrix"),
    use_container_width=True)

est = model[-1] if hasattr(model, "steps") else model
if hasattr(est, "feature_importances_"):
    imp = pd.Series(est.feature_importances_, IRIS_FEATURES).sort_values()
    c2.plotly_chart(px.bar(imp, orientation="h", title="Feature importance",
                           labels={"value": "importance", "index": ""}).update_layout(showlegend=False),
                    use_container_width=True)
else:
    c2.plotly_chart(
        px.scatter_3d(df, x="PetalLengthCm", y="PetalWidthCm", z="SepalLengthCm",
                      color="Species", color_discrete_map=IRIS_COLORS, height=420,
                      title="Species in 3D feature space"),
        use_container_width=True)

# --- 3. predict -------------------------------------------------------------------
st.subheader("3. Predict a new flower")
st.caption("Move the sliders to describe a flower; the model updates instantly.")
cols = st.columns(4)
sample = {f: cols[i].slider(f, float(X[f].min()), float(X[f].max()), float(X[f].median()), 0.1)
          for i, f in enumerate(IRIS_FEATURES)}
sample_df = pd.DataFrame([sample])
proba = pd.Series(model.predict_proba(sample_df)[0], model.classes_)
best = proba.idxmax()

c1, c2 = st.columns([1, 2])
c1.metric("Predicted species", best.capitalize(), f"{proba[best]:.0%} confident", delta_color="off")
c2.plotly_chart(
    px.bar(proba, orientation="h", color=proba.index, color_discrete_map=IRIS_COLORS,
           range_x=[0, 1], height=220, labels={"value": "probability", "index": ""})
    .update_layout(showlegend=False, margin=dict(t=10, b=10)),
    use_container_width=True)

st.divider()
ai.insight_button(
    "Explain these results",
    f"I trained a {model_name} on the Iris dataset. Explain the results to a beginner: what the "
    "accuracy and confusion matrix mean, why some species get confused, and why the model "
    f"predicts '{best}' for my sample flower.",
    f"Cross-validation scores:\n{scores.round(3).to_string(index=False)}\n\n"
    f"Test accuracy: {acc:.3f} on {len(y_te)} flowers.\nConfusion matrix (rows=actual, "
    f"cols=predicted, order {labels}):\n{confusion_matrix(y_te, pred, labels=labels)}\n\n"
    f"Sample flower: {sample}\nPredicted probabilities: {proba.round(3).to_dict()}\n\n"
    f"Species means:\n{df.groupby('Species')[IRIS_FEATURES].mean().round(2).to_string()}",
    key="clf_insight",
)

ui.footer()
