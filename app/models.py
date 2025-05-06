from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    senha = Column(String(255))
    usuario = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    memes = relationship("Meme", back_populates="owner")


class Meme(Base):
    __tablename__ = "memes"
    
    id = Column(Integer, primary_key=True, index=True)
    frase = Column(String(255))
    caminho_imagem = Column(String(255))
    posicao = Column(String(255))


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(255), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
