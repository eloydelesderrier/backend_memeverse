from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app import auth, models, schemas, utils, database



router = APIRouter(tags=["meme"])


@router.post("/meme")
async def criar_meme(
    frase: str = Form(...),
    posicao: str = Form(...),
    imagem: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    token: str = Depends(auth.oauth2_scheme),
    db: Session = Depends(database.get_db)
):
    imagem_bytes = await imagem.read()
    token_data = auth.get_current_user(token, db)
    path = utils.create_meme(frase, posicao, imagem_bytes)
    meme = auth.create_memes(db, frase, path, posicao, current_user.id)
    if not meme:
        raise HTTPException(status_code=400, detail="Erro ao criar meme")
    
    if not token_data:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return meme


@router.get("/memes/{meme_id}")
def get_meme_image(meme_id: int, db: Session = Depends(database.get_db)):
    meme = db.query(models.Meme).filter(models.Meme.id == meme_id).first()
    if meme:
        return FileResponse(meme.caminho_imagem)
    return {"error": "Meme not found"}


@router.delete("/memes/{meme_id}")
def delete_meme(
    meme_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: models.User = Depends(auth.get_current_user), 
    token: str = Depends(auth.oauth2_scheme)
):
    token_data = auth.get_current_user(token, db)
    if not token_data:
        raise HTTPException(status_code=401, detail="Token inválido")
    current_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    meme = db.query(models.Meme).filter(models.Meme.id == meme_id).first()
    if not meme:
        raise HTTPException(status_code=404, detail="Meme não encontrado")

    db.delete(meme)
    db.commit()
    return {"message": "Meme deletado com sucesso"}
