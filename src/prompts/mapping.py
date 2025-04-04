__all__ = ["mapping_template"]

from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import StrictUndefined


env = Environment(
    loader=FileSystemLoader("static/templates/mapping"),
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=StrictUndefined,
)

mapping_messages = [
    ChatMessage(
        content=env.get_template("system.j2").render(),
        role=MessageRole.SYSTEM,
    ),
    ChatMessage(
        content="<explanation>{explanation}</explanation>\n<file_tree>{file_tree}</file_tree>",
        role=MessageRole.USER,
    ),
]

mapping_template = ChatPromptTemplate(message_templates=mapping_messages)
