from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, DateTime, Boolean


class User(BaseModel, Base):
    __tablename__ = 'users'
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    location = Column(String(255), nullable=False, default='KENYA')
    password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize the user"""
        super().__init__(*args, **kwargs)
