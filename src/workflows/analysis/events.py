from llama_index.core.workflow import Event, StartEvent
from src.modules.structure_output import Graph

class InfoEvent(StartEvent):
    repo: str
    owner: str

class GithubEvent(Event):
    file_tree: str
    readme: str


class InstructionEvent(Event):
    explanation: str


class MappingEvent(Event):
    component_mapping: str


class GraphEvent(Event):
    graph: Graph
