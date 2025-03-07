import pickle
from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    Context,
    step,
)
from llama_index.llms.ollama import Ollama
from llama_index.core import Document

from llama_index.readers.github import GithubClient, GithubRepositoryReader
from llama_index.core import Document, PropertyGraphIndex
from llama_index.core.node_parser import CodeSplitter

from app.models.analysis_cache import GithubCache, PGICache


class CodeCloneEvent(Event):
    docs: list[Document]


class CodeCloneCacheEvent(Event):
    docs: list[Document]


class PGICacheEvent(Event):
    pgi: PropertyGraphIndex


class Progress(Event):
    msg: str


class AnalysisFlow(Workflow):
    llm = Ollama("llama3.2")

    @step
    async def get_code(self, ctx: Context, ev: StartEvent) -> CodeCloneEvent:

        try:
            ctx.write_event_to_stream(Progress(msg="Cloning code..."))

            REPO = ev.repo
            OWNER = ev.owner
            BRANCH = ev.branch
            TOKEN = ev.token

            await ctx.set("repo", REPO)
            await ctx.set("owner", OWNER)
            await ctx.set("branch", BRANCH)
            await ctx.set("token", TOKEN)

            ctx.write_event_to_stream(Progress(msg="Attempting restore from cache..."))

            cache = await GithubCache.find_one(
                {
                    "repo": REPO,
                    "owner": OWNER,
                    "branch": BRANCH,
                    "token_hash": TOKEN,
                }
            )
            print("past this")

            if cache:
                ctx.write_event_to_stream(
                    Progress(msg="Cache found! Skipping redundant caching...")
                )

                return CodeCloneCacheEvent(docs=cache.docs)
            else:
                ctx.write_event_to_stream(
                    Progress(msg="Cache was not found, starting code cloning...")
                )

            github_client = GithubClient(github_token=TOKEN)

            reader = GithubRepositoryReader(
                github_client=github_client,
                owner=OWNER,
                repo=REPO,
                filter_file_extensions=(
                    ".java",
                    GithubRepositoryReader.FilterType.INCLUDE,
                ),
                concurrent_requests=5,
            )

            docs = reader.load_data(branch=BRANCH)
            docs = list(
                filter(
                    lambda d: d.metadata["file_name"].endswith(".java"),
                    docs,
                )
            )

            ctx.write_event_to_stream(Progress(msg="Code cloned!"))

            return CodeCloneEvent(
                docs=docs,
            )
        except Exception as e:
            print(e)

    @step
    async def cache_code(self, ctx: Context, ev: CodeCloneEvent) -> CodeCloneCacheEvent:
        ctx.write_event_to_stream(Progress(msg="Caching code..."))
        try:
            cache = GithubCache(
                docs=ev.docs,
                repo=await ctx.get("repo"),
                owner=await ctx.get("owner"),
                branch=await ctx.get("branch"),
                token_hash=await ctx.get("token"),
            )

            await cache.insert()
        except Exception as e:
            print(type(e), e)

        return CodeCloneCacheEvent(
            docs=ev.docs,
        )

    @step
    async def build_pgi(
        self, ctx: Context, ev: CodeCloneCacheEvent
    ) -> PGICacheEvent | StopEvent:
        ctx.write_event_to_stream(Progress(msg="Building pgi..."))

        ctx.write_event_to_stream(Progress(msg="Attempting restore from cache..."))

        cache = await PGICache.find_one(
            {
                "repo": await ctx.get("repo"),
                "owner": await ctx.get("owner"),
                "branch": await ctx.get("branch"),
                "token_hash": await ctx.get("token"),
            }
        )

        if cache:

            ctx.write_event_to_stream(
                Progress(msg="Cache found! Skipping redundant caching...")
            )

            try:
                return StopEvent(result=pickle.loads(cache.pgi))
            except Exception as e:
                print(e)

        docs = ev.docs

        index = PropertyGraphIndex.from_documents(
            docs,
            transformations=[CodeSplitter("java")],
            use_async=True,
            llm=self.llm,
        )

        return PGICacheEvent(pgi=index)

    @step
    async def cache_pgi(self, ctx: Context, ev: PGICacheEvent) -> StopEvent:
        ctx.write_event_to_stream(Progress(msg="Caching pgi..."))

        pgi = ev.pgi

        try:
            cache = PGICache(
                pgi=pickle.dumps(pgi),
                repo=await ctx.get("repo"),
                owner=await ctx.get("owner"),
                branch=await ctx.get("branch"),
                token_hash=await ctx.get("token"),
            )

            await cache.insert()

        except Exception as e:
            print(type(e), e)

        return StopEvent(result=pgi)
