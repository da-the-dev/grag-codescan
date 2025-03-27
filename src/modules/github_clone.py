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


def github_clone(
    repo: str,
    owner: str,
    branch: str,
    token: str,
    verbose=False,
    concurrent_requests=10,
):
    github_client = GithubClient(github_token=token)

    reader = GithubRepositoryReader(
        github_client=github_client,
        owner=owner,
        repo=repo,
        # filter_file_extensions=(
        #     ".java",
        #     GithubRepositoryReader.FilterType.INCLUDE,
        # ),
        verbose=verbose,
        concurrent_requests=concurrent_requests,
    )
    try:
        res = reader.load_data(branch=branch)
        
        return res
    except KeyError as ke:
        if ('commit' in str(ke)):
            raise ValueError("Github token is invalid")
