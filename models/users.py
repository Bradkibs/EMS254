from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, DateTime, Boolean


class User(BaseModel, Base):
    __tablename__ = 'users'
    
    email = Column(String(80), nullable=False)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    phone_number = Column(String(80), nullable=False)
    location = Column(String(80), nullable=False)
    password = Column(String(80), nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
