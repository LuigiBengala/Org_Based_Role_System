from fastapi import HTTPException, status
from passlib.context import CryptContext

from . import schemas

pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def check_user_role(current_user_role: schemas.RoleEnum, role: schemas.RoleEnum):
    if current_user_role != role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")