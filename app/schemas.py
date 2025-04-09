from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class PostCreate(BaseModel):
    content: str

class PostOut(BaseModel):
    id: int
    content: str
    username: str
    created_at: str

    class config:
        orm_mode = True