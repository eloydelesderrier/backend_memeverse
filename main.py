from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.meme.memeverse import router as meme_router
from app import models


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ajuste conforme o frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Inclui as rotas de meme
app.include_router(meme_router, prefix="/criar-meme", tags=["meme"])