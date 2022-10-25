from fastapi import FastAPI
from routers.conversations import conversations_router
from routers.topics import topics_router
from routers.categories import categories_router
from routers.users import users_router


app = FastAPI()
app.include_router(conversations_router)
app.include_router(topics_router)
app.include_router(categories_router)
app.include_router(users_router)
