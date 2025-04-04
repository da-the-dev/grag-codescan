from pydantic import BaseModel, Field


class Triplet(BaseModel):
    node_from: str = Field(..., strict=True)
    relation: str = Field(..., strict=True)
    node_to: str = Field(..., strict=True)


class Graph(BaseModel):
    triplets: list[Triplet]