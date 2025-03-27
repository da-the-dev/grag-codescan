import gradio as gr
from typing import Any

__all__ = "graph"


def foo(text):
    return str(int(text) + 1)


# You take a sidebar as a list of gr components. You can access them and get data
def graph(sidebar: dict[str, Any]):
    with gr.Tab("Graph") as graph:
        # If sidebar exports a gr.Textbox variable "text"
        # you can pass it to other components
        # gr.Markdown(lambda t: f"# Graph for {t}", inputs=sidebar['repo'])
        gr.Markdown(lambda t: f"# Graph for {t}", inputs=sidebar["repo"])

        # You can even setup events
        text = gr.Markdown("1")
        sidebar["run"].click(fn=foo, inputs=text, outputs=text)
        
        # If you click the sidebar button, the `text` component will update

    return locals()
