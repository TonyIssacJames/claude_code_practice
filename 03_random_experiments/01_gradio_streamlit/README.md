# Text Analyzer — Gradio vs. Streamlit

The **same** app (a text statistics tool) built twice, so you can compare how
the two most popular "build a web UI in pure Python" libraries work.

## What the app does

You type/paste text, and it shows:
- word count
- character count (with and without spaces)
- sentence count
- the longest word

## Files

| File               | Purpose                                                        |
| ------------------ | -------------------------------------------------------------- |
| `analyzer.py`      | The shared logic. **No UI code** — just `analyze_text()`.      |
| `gradio_app.py`    | The Gradio UI. Imports `analyze_text`.                         |
| `streamlit_app.py` | The Streamlit UI. Imports `analyze_text`.                      |
| `requirements.txt` | The two libraries to install.                                  |

Because the analysis lives in `analyzer.py`, the two app files differ **only**
in their UI code — that's the part worth comparing.

## Setup

```bash
pip install -r requirements.txt
```

(Optionally create a virtual environment first: `python -m venv .venv` then
activate it.)

## Run the Gradio app

```bash
python gradio_app.py
```

Then open the printed URL (usually <http://127.0.0.1:7860>).

## Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

It opens your browser automatically (usually <http://localhost:8501>).

> Note the difference: Gradio apps are launched like a **normal Python script**
> (`python ...`). Streamlit apps are launched through the **`streamlit` command**,
> which runs your script in a special way (see below).

## The key difference in how they think

**Gradio** — you describe *components* (inputs and outputs) and wire them to a
*function*. Gradio builds the page and calls your function when inputs change,
feeding the return values into the outputs. You never manage the page yourself.

**Streamlit** — you write a *script* that draws the page top-to-bottom. Streamlit
**re-runs the whole script** on every interaction. A widget like `st.text_area()`
both draws the box *and* returns its current value, so data just flows down the
script as normal Python.

| Aspect          | Gradio                              | Streamlit                          |
| --------------- | ----------------------------------- | ---------------------------------- |
| Mental model    | Function ↔ input/output components  | Script re-run top to bottom        |
| How to launch   | `python gradio_app.py`              | `streamlit run streamlit_app.py`   |
| Best known for  | ML model demos, quick API frontends | Data dashboards & internal tools   |

Open both `gradio_app.py` and `streamlit_app.py` side by side — the comments in
each explain the moving parts.
