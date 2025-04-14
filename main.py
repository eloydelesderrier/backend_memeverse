from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.meme.memeverse import router as meme_router
# from app.auth.routes import router as auth_router
# from app.feed.routes import router as feed_router
# from app.database import Base, engine
from app.meme.memeverse import router as meme_router


# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ajuste conforme o frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Inclui as rotas de meme
# app.include_router(auth_router, prefix="/auth", tags=["Autenticação"])
# app.include_router(feed_router, tags=["Feed"])
app.include_router(meme_router, prefix="/meme", tags=["Memes"])