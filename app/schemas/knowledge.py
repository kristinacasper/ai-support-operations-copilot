from pydantic import BaseModel, ConfigDict


class KnowledgeArticleRead(BaseModel):
    id: int
    title: str
    topic: str
    content: str
    active: bool

    model_config = ConfigDict(from_attributes=True)
