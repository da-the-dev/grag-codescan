import gradio as gr
from src.settings import settings


__all__ = "sidebar"


def sidebar():
    with gr.Sidebar():
        repo = gr.Textbox(
            value=settings.sidebar.REPO or "",
            label="Repo name",
            max_lines=1,
            interactive=True,
        )
        owner = gr.Textbox(
            value=settings.sidebar.OWNER or "",
            label="Owner",
            max_lines=1,
            interactive=True,
        )
        # branch = gr.Textbox(
        #     value=settings.sidebar.BRANCH or "",
        #     label="Branch name",
        #     max_lines=1,
        #     interactive=True,
        # )
        # token = gr.Textbox(
        #     value=settings.sidebar.TOKEN or "",
        #     label="Token",
        #     type="password",
        #     max_lines=1,
        #     interactive=True,
        # )

    return locals()
