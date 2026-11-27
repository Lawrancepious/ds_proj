# Iris & Titanic: Interactive Data Science App

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://lawrancepious-ds-proj-app-uiywhr.streamlit.app/)

**Live app: https://lawrancepious-ds-proj-app-uiywhr.streamlit.app/**

An interactive [Streamlit](https://streamlit.io) app that explores two classic datasets, trains
machine-learning models in the browser, and lets you **chat with the data using Google Gemini**.

It began as an internship project (2023) and was later rebuilt with richer dashboards, an ML page,
and AI features.

## Features

| Page | What it does |
|---|---|
| **Overview** | Key numbers for both datasets and quick links. |
| **Iris dashboard** | Filter by species. Histograms, box and violin plots, scatter matrix, correlation heatmap, per-species statistics, CSV download. |
| **Titanic dashboard** | Sidebar filters (sex, class, port). Age and fare distributions, class/sex/age sunburst, passenger titles extracted from names, family-size analysis, CSV download. |
| **Iris classifier** | Compares 5 models with 5-fold cross-validation, trains the one you pick, and shows a confusion matrix and feature importance. Sliders let you describe a new flower and get a live prediction. |
| **Ask your data** | A chat with Gemini. The full dataset is sent as context, so answers come from the actual rows. |

Each dashboard and the classifier also has an **AI insights** button, where Gemini explains what the current charts or model results mean.

### Look & feel

- A dark theme with crimson accents (`.streamlit/config.toml`), the Poppins font, and a red chart palette.
- Animated red gradient banners on every page, with a light sweep and a floating icon.
- Cards fade in and lift on hover, and metric cards appear one after another.
- Buttons glow, and tab underlines slide.
- Gemini answers stream in word by word, and a toast pops up when they finish.
- Balloons greet you on first visit and celebrate a 100% test score. The Titanic page opens with snow.
- Animations turn off automatically if your system has *reduce motion* enabled.

All custom styling lives in [`core/ui.py`](core/ui.py).

## Quick start

```bash
git clone https://github.com/Lawrancepious/ds_proj.git
cd ds_proj
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app opens at http://localhost:8501.

### Enabling the AI features

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey).
2. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and paste in your key:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
   Or set the `GEMINI_API_KEY` environment variable, or paste the key into the sidebar while the app is running.

`secrets.toml` is listed in `.gitignore`, so your key is never committed.
Everything except the AI buttons and the chat works without a key.

## Project structure

```
app.py                    # entry point: page navigation
core/
  data.py                 # cached loaders + Titanic feature engineering
  ai.py                   # Gemini client, streaming, key handling, model fallback
  ui.py                   # theme CSS + animations, hero banners, footer
views/
  home.py
  iris_dashboard.py
  titanic_dashboard.py
  iris_classifier.py
  ask_ai.py
resources/                # datasets and images
.streamlit/
  config.toml             # red dark theme, fonts, chart palette
  secrets.toml.example    # template for your API key
```

## Data

- **`Iris.csv`**: Fisher's 1936 iris dataset. 150 flowers, 3 species, 4 measurements in cm.
- **`test.csv`**: the Kaggle Titanic *test* split, 418 passengers.
- **`gender_submission.csv`**: Kaggle's sample submission.

> **Note on the Titanic data:** `test.csv` has no real survival labels.
> `gender_submission.csv` is a naive baseline that predicts *every woman survived and every man
> died* (about 76.6% accuracy on Kaggle's hidden labels). The app shows it as a baseline only,
> never as ground truth. To build a real survival model, add Kaggle's `train.csv`.

Engineered Titanic features: `Title` (Mr/Mrs/Miss/Master/Rare), `FamilySize`, `TravelType`,
`Deck`, `AgeGroup`, `Class`, `Port`.

## Tech stack

Python · Streamlit · pandas · Plotly · scikit-learn · Google Gemini (`google-genai`)

## Ideas for next steps

- Add Kaggle's `train.csv` and a real Titanic survival model.
- Add Gemini to the live app by putting the key under *App settings → Secrets* on Streamlit Community Cloud.
- Let Gemini generate and run pandas code for exact answers on larger datasets.
