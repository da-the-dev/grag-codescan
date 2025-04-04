__all__ = "graph"
import gradio as gr
from typing import Any

from src.workflows import AnalysisFlow


def graph(sidebar: dict[str, Any]):
    with gr.Tab("Graph"):
        gr.Markdown(lambda t: f"# Graph for {t}", inputs=sidebar["repo"])

        graph_output = gr.HTML(label="Graph Visualization", padding=False)

        visualize_btn = gr.Button("Visualize Graph")

        repo = sidebar["repo"]
        owner = sidebar["owner"]

        async def handler(repo, owner):

            w = AnalysisFlow(timeout=30)
            results = await w.run(
                repo=repo,
                owner=owner,
            )

            return results

        visualize_btn.click(
            handler,
            inputs=[repo, owner],
            outputs=graph_output,
        )

    return locals()
