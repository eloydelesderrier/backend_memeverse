from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, auth, database
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(
    tags=["user"]
)

@router.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.usuario == user.usuario).first()
    if db_user:
        raise HTTPException(status_code=400, detail="usuário já existe")
    
    new_user = models.User(
        usuario=user.usuario,
        senha=auth.hash_password(user.senha)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuario registrado com sucesso"}


@router.post("/login")
def login_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.usuario == user.usuario).first()
    if not db_user or not auth.verify_password(user.senha, db_user.senha):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = auth.create_token(data={"sub": db_user.usuario})
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/user/update")
def update_user(User: schemas.UserUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if User.usuario:
       current_user.usuario = User.usuario
    if User.senha:
        current_user.senha = auth.hash_password(User.senha)
    
    db.commit()
    db.refresh(current_user)
    return {"message": "Usuário atualizado com sucesso"}
   

@router.delete("/user/delete")
def delete_user(User: schemas.UserDelete, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_user = db.query(models.User).filter(models.User.id == User.id).first()
    db.delete(db_user)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}


@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(
        OAuth2PasswordRequestForm),

    db: Session = Depends(database.get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    access_token = auth.create_token(data={"sub": user.usuario})
    return {"access_token": access_token, "token_type": "bearer"}