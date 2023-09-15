from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, DateTime, Boolean, Enum as SQLAlchemyEnum

class User(BaseModel, Base):
    __tablename__ = 'users'
    email = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    location = Column(String(255), nullable=False, default='KENYA')
    password = Column(String(255), nullable=False)
    role = Column(SQLAlchemyEnum('admin', 'user', 'customer_service', name='user_role_enum'), default='user', nullable=False)
    is_active = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize the user"""
        super().__init__(*args, **kwargs)
