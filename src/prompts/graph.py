__all__ = ["graph_template"]

from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage, MessageRole


graph_messages = [
    ChatMessage(
        content="""
Create a system design diagram as a graph of triplets based on the project's component mappings and architecture.

1. **Nodes**: Use ONLY component names from the <component_mapping> (e.g., 'core', 'api', 'plugins'). No technical terms like "database" unless explicitly listed in mappings.
2. **Connections**: Use specific relationship verbs showing directionality:
   - "calls" (API endpoint invocation)
   - "processes data for" (data flow)
   - "extends functionality of" (plugin relationships)
   - "persists data to" (database interactions)
   - "depends on" (library/module dependencies)
3. Keep connections concise (2-4 words max).
4. Focus on direct relationships - avoid chaining (A→B→C should be two separate triplets).
5. Triplets must be triplets, i.e. have the 3 s

Example output:
```
<graph>
(core,provides image processing to,api)
(api,receives requests from,frontend)
(plugins,add audio analysis to,core)
(core,uses dependency injection for,plugins)
</graph>
    """,
        role=MessageRole.SYSTEM,
    ),
    ChatMessage(
        content="<explanation>{explanation}</explanation>\n<component_mapping>{component_mapping}</component_mapping>",
        role=MessageRole.USER,
    ),
]

graph_template = ChatPromptTemplate(message_templates=graph_messages)
