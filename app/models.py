from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base
from .schemas import RoleEnum

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    
class Study(Base):
    __tablename__ = "studies"
    
    id = Column(String, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    organization_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    
    organization = relationship("Organization")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, nullable=False)
    study_id = Column(ForeignKey("studies.id"), nullable=False)
    participant_id = Column(ForeignKey("users.id"), nullable=False)
    scheduled_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.participant)
    
    organization_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)
    
    organization = relationship("Organization")