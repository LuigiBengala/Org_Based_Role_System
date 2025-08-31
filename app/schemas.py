from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import Optional

class OrganizationBase(BaseModel):
    id: str
    name: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationEdit(BaseModel):
    name: str

class Organization(OrganizationBase):
    class Config:
        from_attributes = True
        
class RoleEnum(str, Enum):
    admin = "admin"
    participant = "participant"
    research_assistant = "Research Assistant"
    study_coordinator = "Study Coordinator" 
        
class UserBase(BaseModel):
    id: str
    email: EmailStr
    password: str
    role: RoleEnum
    org: str

class UserCreate(UserBase):
    pass

class UserEdit(BaseModel):
    role: RoleEnum = None
    org: str = None
    
class UserOut(BaseModel):
    id: str
    email: EmailStr
    role: RoleEnum
    org: str | None
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class StudyCreate(BaseModel):
    id: str
    title: str
    description: str
    org: str

class StudyOut(BaseModel):
    title: str
    description: str
    org: str
    
    class Config:
        from_attributes = True
        
class StudyEdit(BaseModel):
    title: str = None
    description: str = None
    org: str = None


class SessionCreate(BaseModel):
    id: str
    study_id: str
    participant_id: str
    scheduled_time: datetime

class SessionOut(SessionCreate):
    class Config:
        from_attributes = True
        
class SessionEdit(BaseModel):
    participant_id: str = None
    scheduled_time: datetime = None