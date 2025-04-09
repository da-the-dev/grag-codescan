import os
import gradio as gr
from llama_index.core.workflow import (
    Workflow,
    Context,
    StopEvent,
    step,
)
from llama_index.llms.ollama import Ollama

from src.modules.structured_output.mapping import Mapping
from src.modules.structured_output.graph import Graph
from src.modules.github import GitHubService
from src.modules.graph import generate_graph
from src.prompts import (
    instruction_template,
    mapping_template,
    graph_template,
)

from .events import *


class AnalysisFlow(Workflow):
    llm = Ollama(
        "qwen2.5-coder",
        base_url="http://ollama:11434" if os.environ.get("PROD") else "http://localhost:11434",
    )

    @step
    async def get_info(self, ev: InfoEvent) -> GithubEvent | StopEvent:
        owner = ev.owner
        repo = ev.repo

        gr.Info("Extracting repository info...")

        gh_service = GitHubService()

        try:
            readme = gh_service.get_github_readme(username=owner, repo=repo)
            file_tree = gh_service.get_github_file_paths_as_list(
                username=owner, repo=repo
            )

            gr.Success("Repository file tree and README extracted successfully!")

            return GithubEvent(file_tree=file_tree, readme=readme)
        except Exception as e:
            gr.Error(f"Error: {e}")
            return StopEvent(e)

    @step
    async def diagram_instruction(
        self, ev: GithubEvent, ctx: Context
    ) -> InstructionEvent:
        file_tree = ev.file_tree
        readme = ev.readme

        await ctx.set("file_tree", file_tree)

        gr.Info("Started initial analysis...")
        messages = instruction_template.format_messages(
            file_tree=file_tree, readme=readme
        )

        response = await self.llm.achat(messages=messages)
        gr.Success("Initial analysis done!")

        return InstructionEvent(explanation=response.message.content)

    @step
    async def mapping(self, ev: InstructionEvent, ctx: Context) -> MappingEvent:
        explanation = ev.explanation
        file_tree = await ctx.get("file_tree")
        await ctx.set("explanation", explanation)

        gr.Info("Started mapping...")
        messages = mapping_template.format_messages(
            explanation=explanation, file_tree=file_tree
        )

        response = await self.llm.as_structured_llm(output_cls=Mapping).achat(
            messages=messages
        )
        gr.Success("Mapping done!")

        return MappingEvent(component_mapping=response.message.content)

    @step
    async def graph_event(self, ev: MappingEvent, ctx: Context) -> GraphEvent:
        component_mapping = ev.component_mapping
        explanation = await ctx.get("explanation")

        gr.Info("Started graph generation...")
        messages = graph_template.format_messages(
            explanation=explanation, component_mapping=component_mapping
        )

        response = await self.llm.as_structured_llm(output_cls=Graph).achat(
            messages=messages
        )
        gr.Success("Graph generated!")

        graph = response.raw

        return GraphEvent(graph=graph)

    @step
    async def html_diagram(self, ev: GraphEvent) -> StopEvent:
        """
        Generates an HTML diagram based on the triplets extracted in the previous step.

        Args:
            ev (GraphEvent): The event containing the graph.

        Returns:
            DiagramEvent: An event containing the generated HTML diagram as a str.
        """
        graph = ev.graph

        html = generate_graph(graph.triplets)

        return StopEvent(html)
