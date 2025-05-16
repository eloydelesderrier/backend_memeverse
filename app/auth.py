from datetime import datetime, timedelta
import token
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import database, models, schemas
import os
from dotenv import load_dotenv

# Secret key
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, usuario: str):
    return db.query(models.User).filter(models.User.usuario == usuario).first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, usuario: str, senha: str):
    user = get_user(db, usuario)
    if not user or not verify_password(senha, user.senha):
        return False
    return user

def verify_user_exists(db: Session, usuario: str, email: str):
    user = db.query(models.User).filter((models.User.usuario == usuario) | (models.User.email == email)).first()
    return user is not None

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("sub")
        if usuario is None:
            raise credentials_exception
        token_data = schemas.TokenData(usuario=usuario)
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.usuario == token_data.usuario).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_memes(db: Session, frase: str, caminho_imagem: str, posicao: str, user_id: int):
    meme = models.Meme(frase=frase, caminho_imagem=caminho_imagem, posicao=posicao, user_id=user_id)
    db.add(meme)
    db.commit()
    db.refresh(meme)
    return meme

def get_memes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Meme).offset(skip).limit(limit).all()

