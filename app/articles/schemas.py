from datetime import datetime
from pydantic import BaseModel


class CreateArticleSchema(BaseModel):
    title: str
    content: str
    category: str


class ArticleSchema(BaseModel):
    id: int
    title: str
    content: str
    category: str
    author_id: int
    created_at: datetime


class CreateCommentSchema(BaseModel):
    content: str


class CreateComplaintSchema(BaseModel):
    reason: str
    content: str
