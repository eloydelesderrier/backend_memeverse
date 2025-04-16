from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Meme(Base):
    __tablename__ = "memes"
    
    id = Column(Integer, primary_key=True, index=True)
    frase = Column(Text)
    caminho_imagem = Column(String(255))
    posicao = Column(String(255))
