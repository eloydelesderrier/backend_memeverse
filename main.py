
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app import database, models
from app.routes.meme import router as meme_router
from app.routes.users import router as login_router

models.Base.metadata.create_all(bind=database.engine)


app = FastAPI(
    title="Memeverse API",
    description="API for generating and managing memes",
    version="1.0.0",
   
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(meme_router)
app.include_router(login_router)

