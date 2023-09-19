from models.basemodel import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship

class Transactions(BaseModel, Base):

    """ The transactions model
    we keep the senders and receivers in the same table
    and create a foreign key relationship to the users table
    ceate a virtual column for the sender and receiver
    in the users table
    """
    __tablename__ = 'transactions'

    # Define the foreign key relationship to the sender user
    sender_id = Column(String(255), ForeignKey('users.id'), nullable=False)

    # Define the foreign key relationship to the receiver user
    receiver_id = Column(String(255), ForeignKey('users.id'), nullable=False)

    # Amount of the transaction
    amount = Column(Float, nullable=False)

    # Define the sender and receiver relationships
    sender = relationship('User', foreign_keys=[sender_id], backref='sent_transaction')
    receiver = relationship('User', foreign_keys=[receiver_id], backref='received_transaction')
