from pydantic import BaseModel

class MemeCreate(BaseModel):
    frase: str
    posicao: str # topo', 'meio', 'baixo'

class MemeOut(BaseModel):
    id: int
    frase: str
    posicao: str