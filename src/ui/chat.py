import gradio as gr
from typing import Any
from qdrant_client import QdrantClient

from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.chat_engine.types import ChatMode, BaseChatEngine
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding


__all__ = "chat"


def chat_engine(documents: list[Document]):
    client = QdrantClient(
        location=":memory:",
        # host=settings.qdrant.HOST,
        port=6333,
    )

    vector_store = QdrantVectorStore(client=client, collection_name="code")

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=OllamaEmbedding("jinaai/jina-embeddings-v2-base-code"),
    )

    return index.as_chat_engine(
        chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT,
        llm=Ollama("llama3.2"),
    )


def chat(sidebar: dict[str, Any]):
    documents: gr.State = sidebar["documents"]

    with gr.Tab("Chat") as chat:
        gr.Markdown(lambda t: f"# Chat for {t}", inputs=sidebar["repo"])

        @gr.render(inputs=documents)
        def render_chat(documents: list[Document]):
            if not documents or len(documents) <= 0:
                gr.Markdown("# No code to chat with! Use the sidebar to scan some code")
                return

            ce: BaseChatEngine = chat_engine(documents)

            chatbot = gr.Chatbot(type="messages")
            msg = gr.Textbox()
            clear = gr.Button("Clear")

            # Hack to reset the engine
            @clear.click
            def clearer():
                global ce
                ce.reset()

            def user(user_message, history: list):
                return "", history + [{"role": "user", "content": user_message}]

            def bot(history: list):
                bot_message = ce.stream_chat(history[-1]["content"])

                history.append({"role": "assistant", "content": ""})
                for token in bot_message.response_gen:
                    history[-1]["content"] += token
                    yield history

            msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
                bot, chatbot, chatbot
            )
            clear.click(lambda: None, None, chatbot, queue=False)

    return locals()
