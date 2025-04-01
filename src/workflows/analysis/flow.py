from llama_index.core.workflow import (
    Workflow,
    Context,
    step,
)


from llama_index.llms.ollama import Ollama

from src.prompts import (
    instruction_template,
    mapping_template,
    graph_template,
)

from .events import (
    GithubEvent,
    InstructionEvent,
    MappingEvent,
    GraphEvent,
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

        messages = instruction_template.format_messages(
            file_tree=file_tree, readme=readme
        )

        response = await self.llm.achat(messages=messages)

        return InstructionEvent(explanation=response.message.content)

    @step
    async def mapping(self, ev: InstructionEvent, ctx: Context) -> MappingEvent:
        explanation = ev.explanation
        file_tree = ctx.get("file_tree")
        await ctx.set("explanation", explanation)

        messages = mapping_template.format_messages(
            explanation=explanation, file_tree=file_tree
        )

        response = await self.llm.achat(messages=messages)

        return MappingEvent(component_mapping=response.message.content)

    @step
    async def graph_event(self, ev: MappingEvent, ctx: Context) -> GraphEvent:
        # TODO!
        component_mapping = ev.component_mapping
        explanation = ctx.get("explanation")

        # messages = graph_template.format_messages(
        #     explanation=explanation, component_mapping=component_mapping
        # )

        # response = await self.llm.achat(messages=messages)

        # graph_triplets = response.message.content

        graph_triplets = "magic"

        return GraphEvent(graph_triplets=graph_triplets)
