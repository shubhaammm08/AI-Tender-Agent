import uuid
from sqlalchemy import Column, String, ForeignKey, JSON, Date, Boolean, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
from models.base import TimestampMixin

class Tenant(Base, TimestampMixin):
    __tablename__ = "tenants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    plan = Column(String, default="Starter")
    
    users = relationship("User", back_populates="tenant")
    company_profile = relationship("CompanyProfile", back_populates="tenant", uselist=False)

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    
    tenant = relationship("Tenant", back_populates="users")

class CompanyProfile(Base, TimestampMixin):
    __tablename__ = "company_profile"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, unique=True)
    gstin = Column(String)
    pan = Column(String)
    udyam_no = Column(String)
    turnover = Column(Numeric)
    categories = Column(JSON)
    states = Column(JSON)
    
    tenant = relationship("Tenant", back_populates="company_profile")

class Document(Base, TimestampMixin):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    type = Column(String, nullable=False)
    file_key = Column(String, nullable=False)
    issued_on = Column(Date)
    expires_on = Column(Date)
    version = Column(Integer, nullable=False, default=1)
