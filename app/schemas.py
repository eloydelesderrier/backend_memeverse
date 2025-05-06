from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    senha: str
    usuario: str

class UserOut(BaseModel):
    id:int
    email: EmailStr
    usuario: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    jti: Optional[str] = None
class MemeCreate(BaseModel):
    frase: str
    posicao: str  # top, center, bottom

class MemeOut(BaseModel):
    id: int
    frase: str
    caminho_imagem: str
    posicao: str

    class Config:
        from_attributes = True
