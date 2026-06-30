"""Text Analyzer — Streamlit version.

Run it with:
    streamlit run streamlit_app.py

It opens automatically in your browser (usually http://localhost:8501).

THE STREAMLIT MENTAL MODEL
--------------------------
Streamlit re-runs THIS ENTIRE SCRIPT, top to bottom, every time the user
interacts with a widget. You write it like a normal Python script that draws
the page line by line:
  - st.text_area(...) draws a box AND returns its current value
  - st.metric(...) draws a stat on the page
There's no separate "function" wired to "components" like in Gradio — the
script itself IS the app, and the data flows downward as the script runs.
"""

import streamlit as st

from analyzer import analyze_text

# st.* calls render UI elements in the order they execute.
st.title("📝 Text Analyzer (Streamlit)")
st.write("Type some text and see basic statistics about it.")

# A text area widget. Whatever the user has typed is RETURNED here on each rerun.
text = st.text_area(
    "Your text",
    height=200,
    placeholder="Paste or type some text here...",
)

# Plain Python: call the shared analysis function with the widget's value.
stats = analyze_text(text)

# Lay out four metrics across four columns.
col1, col2, col3, col4 = st.columns(4)
col1.metric("Words", stats["word_count"])
col2.metric("Characters", stats["char_count"])
col3.metric("No spaces", stats["char_count_no_spaces"])
col4.metric("Sentences", stats["sentence_count"])

st.write("**Longest word:**", stats["longest_word"] or "—")
