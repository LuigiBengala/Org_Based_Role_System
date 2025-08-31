import os

from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from . import models, schemas, utils
from .database import engine, SessionLocal
from .routers import organization, user, auth, study, session

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    
    admin_id = os.getenv("ADMIN_ID")
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_role = schemas.RoleEnum.admin
    
    admin_exists = db.query(models.User).filter(models.User.id == admin_id).first()
    
    if admin_exists is None:
        hashed_password = utils.hash(admin_password)
        admin_user = models.User(
            id=admin_id,
            email=admin_email,
            password=hashed_password,
            role=admin_role,
            org=None,
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
    yield
    
app = FastAPI(lifespan=lifespan)

models.Base.metadata.create_all(bind=engine)

app.include_router(organization.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(study.router)
app.include_router(session.router)