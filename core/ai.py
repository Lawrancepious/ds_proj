"""Thin wrapper around Google Gemini (google-genai SDK).

The API key is read, in order, from:
  1. .streamlit/secrets.toml  ->  GEMINI_API_KEY = "..."
  2. environment variable     ->  GEMINI_API_KEY (or GOOGLE_API_KEY)
  3. a password box in the sidebar (kept only for the browser session)
"""
from __future__ import annotations

import os

import streamlit as st

# First entry is the default; the rest are fallbacks if a model is busy or retired.
MODELS = ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.1-pro-preview"]

SYSTEM_PROMPT = (
    "You are a friendly senior data scientist helping a student explore a dataset. "
    "Answer using ONLY the data provided. When you give numbers, compute them carefully "
    "from the data and say how you got them. Be concise, use Markdown (short headings, "
    "bullet points, small tables). If the data cannot answer a question, say so plainly."
)


def _configured_key() -> str | None:
    try:
        key = st.secrets.get("GEMINI_API_KEY")
        if key:
            return key
    except Exception:  # no secrets.toml present
        pass
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def sidebar_settings() -> None:
    """Render the AI settings block in the sidebar (call once per page that uses AI)."""
    with st.sidebar:
        st.subheader("AI settings")
        if _configured_key():
            st.caption("Gemini API key loaded from config.")
        else:
            st.text_input("Gemini API key", type="password", key="gemini_key_input",
                          help="Get one at https://aistudio.google.com/apikey")
        st.selectbox("Model", MODELS, key="gemini_model")


def get_api_key() -> str | None:
    return _configured_key() or st.session_state.get("gemini_key_input") or None


@st.cache_resource
def _client(api_key: str):
    from google import genai
    return genai.Client(api_key=api_key)


def _request(prompt: str, context: str, history: list[dict] | None):
    from google.genai import types

    key = get_api_key()
    if not key:
        raise RuntimeError("No Gemini API key configured - add one in the sidebar.")
    contents = []
    for msg in history or []:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
    contents.append(types.Content(role="user", parts=[types.Part(text=prompt)]))
    system = SYSTEM_PROMPT + (f"\n\n--- DATA ---\n{context}" if context else "")
    config = types.GenerateContentConfig(system_instruction=system, temperature=0.3)
    chosen = st.session_state.get("gemini_model", MODELS[0])
    order = [chosen] + [m for m in MODELS if m != chosen]
    return _client(key), contents, config, order


def _retryable(e: Exception) -> bool:
    return any(code in str(e) for code in ("503", "404", "429", "UNAVAILABLE"))


def ask(prompt: str, context: str = "", history: list[dict] | None = None) -> str:
    """Send a prompt (plus optional data context and chat history) and return the full reply."""
    return "".join(ask_stream(prompt, context, history))


def ask_stream(prompt: str, context: str = "", history: list[dict] | None = None):
    """Yield the reply chunk by chunk (for st.write_stream's typing animation).

    Falls back to the next model if one is busy/retired before any text arrived.
    """
    client, contents, config, order = _request(prompt, context, history)
    last_error = None
    for model in order:
        started = False
        try:
            for chunk in client.models.generate_content_stream(
                    model=model, contents=contents, config=config):
                if chunk.text:
                    started = True
                    yield chunk.text
            return
        except Exception as e:
            last_error = e
            if started or not _retryable(e):
                break
    raise RuntimeError(f"Gemini request failed: {last_error}")


def insight_button(label: str, prompt: str, context: str, key: str) -> None:
    """A button that streams Gemini commentary into an animated card."""
    if st.button(label, key=key, icon=":material/auto_awesome:", type="primary"):
        if not get_api_key():
            st.warning("Add a Gemini API key in the sidebar to use AI features.")
            return
        with st.container(border=True):
            try:
                st.session_state[key + "_out"] = st.write_stream(ask_stream(prompt, context))
                st.toast("Insights ready!", icon=":material/auto_awesome:")
            except Exception as e:
                st.error(str(e))
        return
    if st.session_state.get(key + "_out"):
        with st.container(border=True):
            st.markdown(st.session_state[key + "_out"])
