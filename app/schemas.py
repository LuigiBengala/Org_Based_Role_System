from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime

class RoleEnum(str, Enum):
    admin = "admin"
    participant = "participant"
    research_assistant = "Research Assistant"
    study_coordinator = "Study Coordinator" 

'''
    #! Organization
'''

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

'''
    #! User
'''
        
class UserCreate(BaseModel):
    id: str
    email: EmailStr
    password: str
    role: RoleEnum
    organization_id: str

class UserEdit(BaseModel):
    role: RoleEnum = None
    organization_id: str = None
    
class UserOut(BaseModel):
    id: str
    email: EmailStr
    role: RoleEnum
    organization_id: str | None
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
'''
    #! Study
'''
    
class StudyCreate(BaseModel):
    id: str
    title: str
    description: str
    organization_id: str

class StudyOut(BaseModel):
    title: str
    description: str
    organization_id: str
    
    class Config:
        from_attributes = True
        
class StudyEdit(BaseModel):
    title: str = None
    description: str = None
    organization_id: str = None

'''
    #! Session
'''

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

'''
    #! Token
'''

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None