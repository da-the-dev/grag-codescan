import gradio as gr
from typing import Any

__all__ = "chat"

def chat(sidebar: dict[str, Any]):
    with gr.Tab("Chat") as chat:
        gr.Markdown(lambda t: f"# Chat for {t}", inputs=sidebar['repo'])
        
    return locals()
