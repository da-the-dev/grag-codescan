import gradio as gr
from src.settings import settings

__all__ = "sidebar"


def sidebar():
    with gr.Sidebar():
        repo = gr.Textbox(
            value=settings.sidebar.REPO or "",
            label="Repo name",
        )
        owner = gr.Textbox(
            value=settings.sidebar.OWNER or "",
            label="Owner",
        )
        branch = gr.Textbox(
            value=settings.sidebar.BRANCH or "",
            label="Branch name",
        )
        token = gr.Textbox(
            value=settings.sidebar.TOKEN or "",
            label="Token",
            type="password",
        )

        run = gr.Button("Start analysis")

    return locals()
