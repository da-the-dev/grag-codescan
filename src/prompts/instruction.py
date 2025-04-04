__all__ = ["instruction_template"]

from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import StrictUndefined


env = Environment(
    loader=FileSystemLoader("static/templates/instruction"),
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=StrictUndefined,
)

instruction_messages = [
    ChatMessage(
        content=env.get_template("system.j2").render(),
        role=MessageRole.SYSTEM,
    ),
    ChatMessage(
        content="<file_tree>{file_tree}</file_tree>\n<readme>{readme}</readme>",
        role=MessageRole.USER,
    ),
]

instruction_template = ChatPromptTemplate(message_templates=instruction_messages)
