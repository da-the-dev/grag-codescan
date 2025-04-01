__all__ = ["mapping_template"]

from llama_index.core import PromptTemplate
from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole


mapping_messages = [
    ChatMessage(
        content="""
You are tasked with mapping key components of a system design to their corresponding files and directories in a project's file structure. You will be provided with a detailed explanation of the system design/architecture and a file tree of the project.

First, carefully read the system design explanation which will be enclosed in <explanation> tags in the users message.

Then, examine the file tree of the project which will be enclosed in <file_tree> tags in the users message.

Your task is to analyze the system design explanation and identify key components, modules, or services mentioned. Then, try your best to map these components to what you believe could be their corresponding directories and files in the provided file tree.

Guidelines:
1. Focus on major components described in the system design.
2. Look for directories and files that clearly correspond to these components.
3. Include both directories and specific files when relevant.
4. If a component doesn't have a clear corresponding file or directory, simply dont include it in the map.

Now, provide your final answer in the following format:

<component_mapping>
1. [Component Name]: [r'regex_to_match_files_from_tree']
2. [Component Name]: [r'regex_to_match_files_from_tree']
[Continue for all identified components]
</component_mapping>

Remember to be as specific as possible in your mappings, only use what is given to you from the file tree, and to strictly follow the components mentioned in the explanation. 
""",
        role=MessageRole.SYSTEM,
    ),
    ChatMessage(
        content="<explanation>{explanation}</explanation>\n<file_tree>{file_tree}</file_tree>",
        role=MessageRole.USER,
    ),
]

mapping_template = ChatPromptTemplate(message_templates=mapping_messages)
