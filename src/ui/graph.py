import gradio as gr
from typing import Any

from src.modules.graph import generate_graph
from src.workflows import AnalysisFlow

__all__ = "graph"


def graph(sidebar: dict[str, Any]):
    with gr.Tab("Graph"):
        header = gr.Markdown(lambda t: f"# Graph for {t}", inputs=sidebar["repo"])

        graph_output = gr.HTML(label="Graph Visualization", padding=False)

        visualize_btn = gr.Button("Visualize Graph")

        file_tree = sidebar["file_tree"]
        readme = sidebar["readme"]

        async def handler(file_tree, readme):
            gr.Info("Started intial analysis...")
            w = AnalysisFlow(timeout=30)
            results = await w.run(
                file_tree=file_tree,
                readme=readme,
            )

            return results

        visualize_btn.click(
            handler,
            inputs=[file_tree, readme],
            outputs=graph_output,
        )

    return locals()
