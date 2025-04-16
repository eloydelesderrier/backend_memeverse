from pydantic import BaseModel

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
