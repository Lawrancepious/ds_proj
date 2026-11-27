"""Data loading and feature engineering shared by every page."""
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "resources"

IRIS_FEATURES = ["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm"]
IRIS_COLORS = {"setosa": "#E63946", "versicolor": "#F4A261", "virginica": "#A8DADC"}


@st.cache_data
def load_iris() -> pd.DataFrame:
    df = pd.read_csv(RESOURCES / "Iris.csv")
    # "Iris-setosa" -> "setosa": shorter labels read better on charts
    df["Species"] = df["Species"].str.replace("Iris-", "", regex=False)
    return df


def _title(name: str) -> str:
    """Pull the honorific out of 'Surname, Title. Given names'."""
    title = name.split(",")[1].split(".")[0].strip()
    title = {"Ms": "Miss", "Mlle": "Miss", "Mme": "Mrs"}.get(title, title)
    return title if title in {"Mr", "Mrs", "Miss", "Master"} else "Rare"


@st.cache_data
def load_titanic() -> pd.DataFrame:
    df = pd.read_csv(RESOURCES / "test.csv")
    baseline = pd.read_csv(RESOURCES / "gender_submission.csv")
    df = df.merge(baseline.rename(columns={"Survived": "BaselinePrediction"}),
                  on="PassengerId", how="left")

    df["Title"] = df["Name"].map(_title)
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["TravelType"] = np.where(df["FamilySize"] == 1, "Alone", "With family")
    df["Deck"] = df["Cabin"].str[0].fillna("Unknown")
    df["AgeGroup"] = pd.cut(
        df["Age"], bins=[0, 12, 18, 30, 45, 60, 100],
        labels=["Child (0-12)", "Teen (13-18)", "Young adult (19-30)",
                "Adult (31-45)", "Middle-aged (46-60)", "Senior (60+)"],
    ).astype(str).replace("nan", "Unknown")
    df["Class"] = df["Pclass"].map({1: "1st", 2: "2nd", 3: "3rd"})
    df["Port"] = df["Embarked"].map({"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"})
    return df


def dataset_context(name: str) -> str:
    """A compact text description of a dataset (schema, stats, full CSV) for the LLM."""
    if name == "Iris":
        df = load_iris()
        notes = ("Classic Iris flower dataset (Fisher, 1936): 150 flowers, 3 species, "
                 "4 measurements in centimetres.")
    else:
        df = load_titanic().drop(columns=["Name", "Ticket"])
        notes = (
            "Titanic passengers from the Kaggle *test* split (418 passengers). It has NO real "
            "survival labels. 'BaselinePrediction' comes from Kaggle's gender_submission.csv, "
            "a naive baseline that predicts every woman survived and every man died - it is NOT "
            "ground truth, so never present it as actual survival. Engineered columns: Title, "
            "FamilySize, TravelType, Deck, AgeGroup, Class, Port."
        )
    return (
        f"DATASET: {name}\n{notes}\n\n"
        f"Shape: {df.shape[0]} rows x {df.shape[1]} columns\n\n"
        f"Missing values per column:\n{df.isna().sum().to_string()}\n\n"
        f"Summary statistics:\n{df.describe(include='all').round(2).to_string()}\n\n"
        f"Full data (CSV):\n{df.to_csv(index=False)}"
    )
