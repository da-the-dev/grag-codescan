import gradio as gr
from typing import Any

from src.modules.graph import extract_triplets, generate_graph

__all__ = "graph"


# You take a sidebar as a list of gr components. You can access them and get data
def graph(sidebar: dict[str, Any]):
    with gr.Tab("Graph"):
        header = gr.Markdown(lambda t: f"# Graph for {t}", inputs=sidebar["repo"])

        text = gr.Markdown("1")
        graph_output = gr.HTML(label="Graph Visualization", padding=False)

        visualize_btn = gr.Button("Visualize Graph")

        # mock

        text = """
        Some possible text
        (backend, communicate, frontend)
        (frontend, communicate, backend)
        (backend, communicate, database)
        """
        # triplets = [
        #     ("backend", "communicate", "frontend"),
        #     ("frontend", "communicate", "backend"),
        #     ("backend", "communicate", "database"),
        # ]
        text = """
        (API, processes requests from clients, Core Functionality)
        (Core Functionality, interacts with Plugins to load and manage plugins, Task System)
        (Task System, coordinates tasks between Core Functionality and Plugins, Audio Processing)
        (Audio Processing, handles audio file processing, Text Processing)
        (Text Processing, handles text file processing, Plugin Loader)
        (Plugin Loader, loads and manages plugins for Core Functionality, API)
        (API, uses Core Functionality to process tasks, interacts with external services such as speech recognition APIs)

        (API, processes requests from clients -> Core Functionality, coordinates tasks between components)
        (Core Functionality, interacts with Plugins to load and manage plugins -> Task System, coordinates tasks between components)
        (Task System, coordinates tasks between Core Functionality and Plugins -> Audio Processing, handles audio file processing)
        (Audio Processing, handles audio file processing -> Text Processing, handles text file processing)
        (Text Processing, handles text file processing -> Plugin Loader, loads and manages plugins for Core Functionality)
        (Plugin Loader, loads and manages plugins for Core Functionality -> API, uses Core Functionality to process tasks)

        (API, interacts with external services such as speech recognition APIs -> Core Functionality, processes tasks using audio and text data)
        (Core Functionality, processes tasks using audio and text data -> Plugins, load and manage plugins to support different languages and features)

        (API, uses Python and Poetry package manager for development and deployment)
        (Core Functionality, uses Ruff linter and Pytest testing framework for code quality and testing)
        (Plugins, use plugin-based architecture to enable flexible support for various languages and features)        
        """
        triplets = extract_triplets(text)
        visualize_btn.click(
            lambda: generate_graph(triplets), inputs=[], outputs=graph_output
        )

    return locals()
