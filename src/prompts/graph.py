__all__ = ["graph_template"]

from llama_index.core import PromptTemplate
from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole


graph_messages = [
    ChatMessage(
        content="""
TODO
    """,
        role=MessageRole.SYSTEM,
    ),
    ChatMessage(
        content="<explanation>{explanation}</explanation>\n<component_mapping>{component_mapping}</component_mapping>",
        role=MessageRole.USER,
    ),
]

graph_template = ChatPromptTemplate(message_templates=graph_messages)
