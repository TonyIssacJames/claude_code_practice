"""Text Analyzer — Gradio version.

Run it with:
    python gradio_app.py

Then open the URL it prints (usually http://127.0.0.1:7860).

THE GRADIO MENTAL MODEL
-----------------------
You describe your UI as a set of *components* (inputs + outputs) and connect
them to a plain Python *function*. Gradio:
  1. builds the web page from your component definitions, and
  2. calls your function whenever the inputs change / a button is clicked,
     then puts the return values into the output components.

You don't write a loop or manage page state — Gradio drives everything.
"""

import gradio as gr

from analyzer import analyze_text


def format_results(text: str):
    """Adapter between Gradio's UI and our shared analyze_text() function.

    Gradio passes the input component's value (the textbox string) as the
    argument, and routes each returned value into one output component, in order.
    """
    stats = analyze_text(text)
    return (
        stats["word_count"],
        stats["char_count"],
        stats["char_count_no_spaces"],
        stats["sentence_count"],
        stats["longest_word"] or "—",
    )


# gr.Interface is the quickest way to wrap a function in a UI:
# - `fn`      : the function to call
# - `inputs`  : the component(s) whose values become the function's arguments
# - `outputs` : the component(s) that display the function's return values
demo = gr.Interface(
    fn=format_results,
    inputs=gr.Textbox(
        lines=8,
        label="Your text",
        placeholder="Paste or type some text here...",
    ),
    outputs=[
        gr.Number(label="Words"),
        gr.Number(label="Characters (with spaces)"),
        gr.Number(label="Characters (no spaces)"),
        gr.Number(label="Sentences"),
        gr.Textbox(label="Longest word"),
    ],
    title="📝 Text Analyzer (Gradio)",
    description="Type some text and see basic statistics about it.",
    live=True,  # re-run on every keystroke instead of needing a Submit button
)


if __name__ == "__main__":
    demo.launch()
