from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_banned: Mapped[bool] = mapped_column(default=False)

    # articles: Mapped[list["Article"]] = relationship("Article", back_populates="author")
    # comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")
