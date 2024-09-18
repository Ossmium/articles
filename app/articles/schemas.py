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


class CommentSchema(BaseModel):
    id: int
    content: str
    author_id: int
    article_id: int
    created_at: datetime


class CreateCommentSchema(BaseModel):
    content: str


class ComplaintSchema(BaseModel):
    id: int
    reason: str
    content: str | None
    article_id: int
    author_id: int
    created_at: datetime


class CreateComplaintSchema(BaseModel):
    reason: str
    content: str


class ReviewSchema(BaseModel):
    id: int
    title: str
    content: str | None
    article_id: int
    author_id: int
    created_at: datetime


class CreateReviewSchema(BaseModel):
    title: str
    content: str | None
