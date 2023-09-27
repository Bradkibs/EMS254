from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship

class Messages(BaseModel, Base):
    """ The messages model"""
    __tablename__ = 'messages'

    content = Column(Text, nullable=False)

    # Define the foreign key relationship to the sender user
    sender_id = Column(String(255), ForeignKey('users.id'), nullable=False)
    receiver_id = Column(String(255), ForeignKey('users.id'), nullable=False)

    # Define the sender and receiver relationships
    sender = relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')
