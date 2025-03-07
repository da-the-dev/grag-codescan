from beanie import Document
from llama_index.core import PropertyGraphIndex, Document as liDocument


class GithubCache(Document):
    docs: list[liDocument]
    repo: str
    owner: str
    branch: str
    token_hash: str

    class Settings:
        name = "github"


class PGICache(Document):
    pgi: bytes
    repo: str
    owner: str
    branch: str
    token_hash: str

    class Settings:
        name = "pgi"
