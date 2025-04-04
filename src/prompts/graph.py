__all__ = ["graph_template"]

from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import StrictUndefined


env = Environment(
    loader=FileSystemLoader("static/templates/graph"),
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=StrictUndefined,
)

graph_messages = [
    ChatMessage(
        content=env.get_template("system.j2").render(),
        role=MessageRole.SYSTEM,
    ),
    ChatMessage(
        content="<explanation>{explanation}</explanation>\n<component_mapping>{component_mapping}</component_mapping>",
        role=MessageRole.USER,
    ),
]

graph_template = ChatPromptTemplate(message_templates=graph_messages)
