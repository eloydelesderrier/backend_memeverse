from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from . import models, schemas, crud, database, utils

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/generate-meme", response_model=schemas.MemeOut)
async def generate_meme(
    frase: str = Form(...),
    posicao: str = Form(...),
    imagem: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    path = utils.generate_meme(await imagem.read(), frase, posicao)
    meme = crud.create_meme(db, frase, path, posicao)
    return meme

# @app.get("/memes", response_model=list[schemas.MemeOut])
# def list_memes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return crud.get_memes(db, skip, limit)

@app.get("/search", response_model=list[schemas.MemeOut])
def search_memes(q: str, db: Session = Depends(get_db)):
    return crud.search_memes(db, q)

@app.get("/meme/{meme_id}")
def get_meme_image(meme_id: int, db: Session = Depends(get_db)):
    meme = db.query(models.Meme).filter(models.Meme.id == meme_id).first()
    if meme:
        return FileResponse(meme.caminho_imagem)
    return {"error": "Meme not found"}
