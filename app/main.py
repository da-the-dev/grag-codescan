import configparser
import pickle
import gradio as gr
from typing import List

from contextlib import asynccontextmanager
from fastapi import FastAPI

from llama_index.core import (
    Settings,
    PropertyGraphIndex,
)
from llama_index.core.chat_engine.types import ChatMode
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.ai.workflow import AnalysisFlow
from app.models.analysis_cache import GithubCache, PGICache

import nest_asyncio

nest_asyncio.apply()

config = configparser.ConfigParser()
config.read("settings.ini")
LLM = config["DEFAULT"]["LLM"]
EMBED_MODEL = config["DEFAULT"]["EMBED_MODEL"]


if gr.NO_RELOAD:
    Settings.llm = Ollama(
        LLM,
        request_timeout=3 * 60,
        # async_mode=True,
    )
    Settings.embed_model = OllamaEmbedding(EMBED_MODEL)


async def create_task(owner, repo, branch, token, run_ids):
    w = AnalysisFlow(timeout=5 * 60)

    handler = w.run(
        owner=owner,
        repo=repo,
        branch=branch,
        token=token,
    )

    async for event in handler.stream_events():
        print(event)

    return run_ids


async def get_pgis():
    return await PGICache.all().to_list()


with gr.Blocks() as demo:
    pgis = gr.State([])
    selected_pgi_idx = gr.State(0)

    with gr.Tab(label="Запуск таски") as page1:
        repo = gr.Textbox(
            value=config['github']["repo"] or "repo",
            label="Repo name",
        )
        owner = gr.Textbox(
            value=config['github']["owner"] or "owner",
            label="Owner",
        )
        branch = gr.Textbox(
            value=config['github']["branch"] or "branch",
            label="Branch name",
        )
        token = gr.Textbox(
            value=config['github']["token"] or "token",
            label="Token",
            type="password",
        )

        analysis_start_btn = gr.Button("Запустить анализ")
        analysis_start_btn.click(
            fn=create_task,
            inputs=[owner, repo, branch, token],
            outputs=[],
        )

    with gr.Tab(label="Просмотр статуса") as page2:

        refresh = gr.Button("Обновить")
        refresh.click(get_pgis, None, pgis)

        @gr.render(
            inputs=[pgis],
            # trigger_mode="multiple",
        )
        def render_task_list(pgis: List[PGICache]):
            if len(pgis) <= 0:
                gr.Textbox("Нет задач!")
                return

            def selectables():
                for pgi in pgis:
                    yield [pgi.repo, pgi.owner]

            task_df = gr.Dataframe(
                list(selectables()),
                headers=["ID", "Статус"],
                interactive=False,
                show_search=False,
            )

            def select_callback(df: list[list[str, str]], evt: gr.SelectData):
                gr.Info(f"Выбран результат!")
                return evt.index[0]

            task_df.select(select_callback, inputs=task_df, outputs=selected_pgi_idx)
            pass

    with gr.Tab(label="Результаты") as page3:

        @gr.render(
            inputs=[pgis, selected_pgi_idx],
            triggers=[page3.select],
        )
        def render_chat(pgis, selected_pgi_idx):
            index: PropertyGraphIndex = pickle.loads(pgis[selected_pgi_idx].pgi)

            print(type(index), index)

            chat_engine = index.as_chat_engine(ChatMode.CONTEXT)

            chatbot = gr.Chatbot(
                type="messages",
                min_height=500,
                show_label=False,
                autoscroll=True,
            )

            with gr.Row():
                with gr.Column(scale=10):
                    msg = gr.Textbox(show_label=False)
                    clear = gr.ClearButton(value="Очистить", components=[msg, chatbot])

            def user(user_message, history: list):
                return "", history + [{"role": "user", "content": user_message}]

            def bot(history: list):
                user_message = history[-1]["content"]

                response_stream = chat_engine.stream_chat(user_message)

                history.append(
                    gr.ChatMessage("", role="assistant", metadata={"title": "Thoughts"})
                )

                for text in response_stream.response_gen:
                    prev = history[-1]
                    prev.content += text

                    if prev.content.startswith("<think>"):
                        prev.content = prev.content[7:]

                    if prev.content.endswith("</think>"):
                        prev.content = prev.content[:-8]
                        break

                    yield history

                history.append(gr.ChatMessage("", role="assistant"))

                for text in response_stream.response_gen:
                    prev = history[-1]
                    prev.content += text

                    yield history

            msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
                bot, chatbot, chatbot
            )


client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["result_cache"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(database=db, document_models=[GithubCache, PGICache])
    print("beanie started")
    yield
    print("stopping")
    


app = FastAPI(lifespan=lifespan)

app = gr.mount_gradio_app(app, demo, path="/")
