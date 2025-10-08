from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import organization, user, auth, study, session
    
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(organization.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(study.router)
app.include_router(session.router)

@app.get("/")
async def main():
    return {"message": "Hellow world!"}