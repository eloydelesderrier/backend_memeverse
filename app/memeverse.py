from fastapi import APIRouter, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app import models, schemas, utils, database, crud



router = APIRouter()


@router.post("/generate-meme", response_model=schemas.MemeOut)
async def generate_meme(
    frase: str = Form(...),
    posicao: str = Form(...),
    imagem: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    path = utils.generate_meme(await imagem.read(), frase, posicao)
    meme = crud.create_meme(db, frase, path, posicao)
    return meme

# @app.get("/memes", response_model=list[schemas.MemeOut])
# def list_memes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return crud.get_memes(db, skip, limit)

@router.get("/search", response_model=list[schemas.MemeOut])
def search_memes(q: str, db: Session = Depends(database.get_db)):
    return crud.search_memes(db, q)

@router.get("/memes/{meme_id}")
def get_meme_image(meme_id: int, db: Session = Depends(database.get_db)):
    meme = db.query(models.Meme).filter(models.Meme.id == meme_id).first()
    if meme:
        return FileResponse(meme.caminho_imagem)
    return {"error": "Meme not found"}