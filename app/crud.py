from sqlalchemy.orm import Session
from . import models, schemas

def create_meme(db: Session, frase: str, caminho_imagem: str, posicao: str):
    meme = models.Meme(frase=frase, caminho_imagem=caminho_imagem, posicao=posicao)
    db.add(meme)
    db.commit()
    db.refresh(meme)
    return meme

def get_memes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Meme).offset(skip).limit(limit).all()

def search_memes(db: Session, query: str):
    return db.query(models.Meme).filter(models.Meme.frase.like(f"%{query}%")).all()
