from pydantic import BaseModel


class Triplet(BaseModel):
    node1: str = ""
    connection: str = ""
    node2: str = ""


class Graph(BaseModel):
    triplets: list[Triplet]
