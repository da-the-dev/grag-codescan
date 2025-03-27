import gradio as gr

from src.modules import (
    graph,
    chat,
    sidebar
)

with gr.Blocks() as demo:
    sb = sidebar()
        
    graph(sb)
    chat(sb) 
    
demo.launch()