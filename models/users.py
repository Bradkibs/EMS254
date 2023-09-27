from models.basemodel import BaseModel, Base
from models.transactions import Transactions
from sqlalchemy import Column, String, DateTime, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

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

    # Define the relationship to the accounts table
    accounts = relationship("Accounts", uselist=False, back_populates="user")

    # Define the relationship to the transactions table
    sent_transactions = relationship('Transactions', foreign_keys=[Transactions.sender_id], back_populates='sender')
    received_transactions = relationship('Transactions', foreign_keys=[Transactions.receiver_id], back_populates='receiver')

    # Define the relationship to the messages table
    sent_messages = relationship('Messages', foreign_keys='Messages.sender_id', back_populates='sender')
    received_messages = relationship('Messages', foreign_keys='Messages.receiver_id', back_populates='receiver')

    def __init__(self, *args, **kwargs):
        """Initialize the user"""
        super().__init__(*args, **kwargs)
