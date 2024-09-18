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
    ArticleSchema,
    CreateArticleSchema,
    CommentSchema,
    CreateCommentSchema,
    ComplaintSchema,
    CreateComplaintSchema,
    ReviewSchema,
    CreateReviewSchema,
)
from app.users.dependencies import get_current_user
from app.logger import logger

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
) -> ArticleSchema:
    article = await ArticleService.add(
        title=article_data.title,
        content=article_data.content,
        category=article_data.category,
        author_id=user.id,
    )

    logger.info(f"Статься #{article.id} создана пользователем #{user.id}")

    return article


@router.get("/{article_id}")
async def get_article(article_id: int) -> ArticleSchema:
    article = await ArticleService.find_by_id(id=article_id)
    if not article:
        logger.error("Попытка получения доступа к несуществующей статье")

        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена",
        )
    return article


@router.delete("/{article_id}/delete")
async def delete_article(
    article_id: int,
    user: Users = Depends(get_current_user),
) -> ArticleSchema:
    article = await ArticleService.find_one_or_none(
        id=article_id,
    )
    if not article:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена",
        )

    if article.author_id == user.id or user.is_admin:
        deleted_article = await ArticleService.delete(id=article_id)

        logger.info(f"Статья #{delete_article.id} удалена пользователем #{user.id}")

        return deleted_article

    logger.error("Попытка удаления статьи")
    raise HTTPException(
        status.HTTP_403_FORBIDDEN,
        detail="Нет прав на удаление",
    )


@router.post("/{article_id}/comments")
async def add_comment_to_article(
    article_id: int,
    comment_data: CreateCommentSchema,
    user: Users = Depends(get_current_user),
) -> CommentSchema:
    article = await ArticleService.find_by_id(id=article_id)
    if not article:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена",
        )

    comment = await CommentService.add(
        content=comment_data.content,
        author_id=user.id,
        article_id=article_id,
    )

    logger.info(f"Пользователь #{user.id} добавил комментарий к статье #{article_id}")

    return comment


@router.delete("/{article_id}/comments/{comment_id}")
async def delete_comment(
    article_id: int,
    comment_id: int,
    user: Users = Depends(get_current_user),
) -> CommentSchema:
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
        deleted_comment = await CommentService.delete(id=comment_id)

        logger.info(
            f"Пользователь #{user.id} удалил комментарий у статьи #{article_id}"
        )

        return deleted_comment

    raise HTTPException(
        status.HTTP_403_FORBIDDEN,
        detail="Нет прав на удаление",
    )


@router.get("/{article_id}/complaints")
async def get_article_complaints(
    article_id: int,
    limit: int = 5,
    offset: int = 0,
    user: Users = Depends(get_current_user),
) -> list[ComplaintSchema]:
    if not user.is_admin:
        logger.error("Попытка получения доступа к жалобам")

        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Нет прав",
        )

    article = await ArticleService.find_by_id(id=article_id)
    if not article:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена",
        )

    complaints = await ComplaintService.find_all(
        limit=limit,
        offset=offset,
        article_id=article_id,
    )

    return complaints


@router.post("/{article_id}/complaints")
async def add_complaint_to_article(
    article_id: int,
    complaint_data: CreateComplaintSchema,
    user: Users = Depends(get_current_user),
) -> ComplaintSchema:
    article = await ArticleService.find_by_id(id=article_id)
    if not article:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена",
        )

    complaint = await ComplaintService.add(
        reason=complaint_data.reason,
        content=complaint_data.content,
        article_id=article_id,
        author_id=user.id,
    )

    logger.info(f"Пользователь #{user.id} пожаловался на статью #{article_id}")

    return complaint


@router.post("/{article_id}/reviews")
async def add_review_to_article(
    article_id: int,
    review_data: CreateReviewSchema,
    user: Users = Depends(get_current_user),
) -> ReviewSchema:
    article = await ArticleService.find_by_id(id=article_id)
    if not article:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Статья не найдена",
        )

    review = await ReviewService.add(
        title=review_data.title,
        content=review_data.content,
        article_id=article_id,
        author_id=user.id,
    )

    logger.info(f"Пользователь #{user.id} добавил отзыв на статью #{article_id}")

    return review
