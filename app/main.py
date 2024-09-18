from fastapi import FastAPI

from app.users.router import auth_router
from app.users.router import users_router
from app.articles.router import router as article_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(article_router)
