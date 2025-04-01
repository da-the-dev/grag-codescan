from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
)

class GithubEvent(StartEvent):
    file_tree: str
    readme: str


class InstructionEvent(Event):
    explanation: str


class MappingEvent(Event):
    component_mapping: str


class GraphEvent(StopEvent):
    graph_triplets: str