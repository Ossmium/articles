from fastapi import APIRouter, Depends, HTTPException, status
from app.users.models import Users
from app.articles.models import (
    Articles,
    Comments,
    Complaints,
    Reviews,
)
from app.articles.service import (
    ArticleService,
    CommentService,
    ComplaintService,
    ReviewService,
)
from app.articles.schemas import (
    CreateArticleSchema,
    ArticleSchema,
    CreateCommentSchema,
    CreateComplaintSchema,
)
from app.users.dependencies import get_current_user

router = APIRouter(
    tags=["Articles"],
    prefix="/articles",
)


@router.get("")
async def get_articles(
    category: str = None, limit: int = 5, offset: int = 0
) -> list[ArticleSchema]:
    return await ArticleService.find_all(
        limit=limit,
        offset=offset,
        category=category,
    )


@router.post("/new")
async def create_article(
    article_data: CreateArticleSchema,
    user: Users = Depends(get_current_user),
):
    await ArticleService.add(
        title=article_data.title,
        content=article_data.content,
        category=article_data.category,
        author_id=user.id,
    )


@router.get("/{article_id}")
async def get_article(article_id: int) -> ArticleSchema:
    article = await ArticleService.find_by_id(id=article_id)
    if not article:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена",
        )
    return article


@router.delete("/{article_id}/delete")
async def delete_article(
    article_id: int,
    user: Users = Depends(get_current_user),
):
    article = await ArticleService.find_one_or_none(
        id=article_id,
    )
    if not article:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена",
        )

    if article.author_id == user.id or user.is_admin:
        await ArticleService.delete(id=article_id)
        return None

    raise HTTPException(
        status.HTTP_403_FORBIDDEN,
        detail="Нет прав на удаление",
    )


@router.post("/{article_id}/comments")
async def add_comment_to_article(
    article_id: int,
    comment: CreateCommentSchema,
    user: Users = Depends(get_current_user),
):
    article = await ArticleService.find_by_id(id=article_id)
    if not article:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена",
        )

    await CommentService.add(
        content=comment.content,
        author_id=user.id,
        article_id=article_id,
    )


@router.delete("/{article_id}/comments/{comment_id}")
async def delete_comment(
    article_id: int,
    comment_id: int,
    user: Users = Depends(get_current_user),
):
    article = await ArticleService.find_by_id(id=article_id)
    if not article:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена",
        )

    comment: Comments = await CommentService.find_by_id(id=comment_id)
    if not comment:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Комментарий не найден",
        )

    if comment.author_id == user.id or user.is_admin:
        await CommentService.delete(id=comment_id)
        return None

    raise HTTPException(
        status.HTTP_403_FORBIDDEN,
        detail="Нет прав на удаление",
    )


@router.post("/{article_id}/complaints")
async def add_complaint_to_article(
    article_id: int,
    complaint: CreateComplaintSchema,
    user: Users = Depends(get_current_user),
):
    article = await ArticleService.find_by_id(id=article_id)
    if not article:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена",
        )

    await ComplaintService.add(
        reason=complaint.reason,
        content=complaint.content,
        article_id=article_id,
        author_id=user.id,
    )
