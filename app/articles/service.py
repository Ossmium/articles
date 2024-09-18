from app.articles.models import Articles, Comments, Reviews, Complaints
from app.service.service import BaseService


class ArticleService(BaseService):
    model = Articles


class CommentService(BaseService):
    model = Comments


class ComplaintService(BaseService):
    model = Complaints


class ReviewService(BaseService):
    model = Reviews
