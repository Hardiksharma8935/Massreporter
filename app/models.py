from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime

Base = declarative_base()

class AuthorizedAccount(Base):
    __tablename__ = 'authorized_accounts'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String, unique=True, nullable=False)
    encrypted_session = Column(LargeBinary, nullable=False)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    target_entity = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
  
