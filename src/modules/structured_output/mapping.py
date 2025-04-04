from pydantic import BaseModel, Field


class Component(BaseModel):
    component_name: str = Field(..., strict=True)
    path_to_component: str = Field(..., strict=True)

class Mapping(BaseModel):
    components: list[Component]