import gradio as gr
from src.settings import settings
from src.modules.github import GitHubService

__all__ = "sidebar"


def get_repo_tree_and_readme(repo, owner, branch, token) -> tuple[str, str]:
    gr.Info("Trying to extract repository code...")

    gh_service = GitHubService()

    try:
        readme = gh_service.get_github_readme(username=owner, repo=repo)
        file_tree = gh_service.get_github_file_paths_as_list(username=owner, repo=repo)

        print(readme, file_tree)

        gr.Success("Repository file tree and readme extracted successfully.")

        return file_tree, readme
    except ValueError as e:
        gr.Error(f"{e}")
        return
    except Exception as e:
        gr.Error(f"Error: {e}")
        return


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

        file_tree = gr.State()
        readme = gr.State()

        file_tree.change(print)
        readme.change(print)

        run.click(
            get_repo_tree_and_readme,
            [
                repo,
                owner,
                branch,
                token,
            ],
            [file_tree, readme],
        )

    return locals()
