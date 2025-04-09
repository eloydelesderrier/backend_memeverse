from sqlalchemy.orm import Session
# from .app import TokenBlacklist
from models import TokenBlacklist

def is_token_blacklisted(db: Session, token: str) -> bool:
    return db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first() is not None

def blacklist_token(db: Session, token: str):
    if not is_token_blacklisted(db, token):
        db_token = TokenBlacklist(token=token)
        db.add(db_token)
        db.commit()