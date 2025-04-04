from llama_index.core.workflow import (
    Workflow,
    Context,
    StopEvent,
    step,
)

import gradio as gr


from llama_index.llms.ollama import Ollama

from src.modules.structure_output import Graph
from src.prompts import (
    instruction_template,
    mapping_template,
    graph_template,
)
from src.modules.graph import generate_graph

from .events import (
    GithubEvent,
    InstructionEvent,
    MappingEvent,
    GraphEvent,
    DiagramEvent,
)


class AnalysisFlow(Workflow):
    llm = Ollama("llama3.2")

    @step
    async def diagram_instruction(
        self, ev: GithubEvent, ctx: Context
    ) -> InstructionEvent:
        file_tree = ev.file_tree
        readme = ev.readme

        await ctx.set("file_tree", file_tree)

        gr.Info("Started intial analysis...")
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

        response = await self.llm.achat(messages=messages)
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
        
        print(html)

        return StopEvent(diagram=html)
