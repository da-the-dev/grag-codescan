import gradio as gr

from src.ui import (
    graph,
    chat,
    sidebar
)

with gr.Blocks() as demo:
    sb = sidebar()
        
    graph(sb)
    chat(sb) 
    
demo.launch(debug=True)
