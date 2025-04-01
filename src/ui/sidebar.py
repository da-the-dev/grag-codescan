import gradio as gr
from src.settings import settings
from src.modules.github_clone import github_clone

__all__ = "sidebar"


def clone_and_notify(r, o, b, t):
    gr.Info("Cloning code...")
    # why is this a tuple?????
    (documents,) = (github_clone(r, o, b, t, True),)
    gr.Success("Done! Check the tabs")

    return documents


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
        branch = gr.Textbox(
            value=settings.sidebar.BRANCH or "",
            label="Branch name",
            max_lines=1,
            interactive=True,
        )
        token = gr.Textbox(
            value=settings.sidebar.TOKEN or "",
            label="Token",
            type="password",
            max_lines=1,
            interactive=True,
        )

        run = gr.Button("Start analysis")

        documents = gr.State()

        run.click(
            clone_and_notify,
            [
                repo,
                owner,
                branch,
                token,
            ],
            documents,
        )

    return locals()
