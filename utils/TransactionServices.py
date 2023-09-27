from models.transactions import Transactions
from db.storage import DB

class TransactionServices:
    __db = DB()
    """class to manage transactions"""

    def create_a_transaction(self, **kwargs):
        """Create a transaction"""
        sender_id = kwargs.get('sender_id')
        receiver_id = kwargs.get('receiver_id')
        amount = kwargs.get('amount')
        transaction = Transactions(sender_id=sender_id, receiver_id=receiver_id, amount=amount)
        self.__db.add(transaction)
        self.__db.save()
        return transaction

    def get_transaction(self, transaction_id):
        """Get a transaction"""
        transaction = self.__db.query(Transactions).filter_by(id=transaction_id).first()
        return transaction

    def delete_transaction(self, transaction_id):
        """Delete a transaction"""
        transaction = self.__db.query(Transactions).filter_by(id=transaction_id).first()
        self.__db.delete(transaction)
        self.__db.save()
        return transaction

    def get_all_transactions(self):
        """Get all transactions"""
        transactions = self.__db.query(Transactions).all()
        return transactions

    def update_transaction(self, transaction_id, **kwargs):
        """Update a transaction"""
        transaction = self.__db.query(Transactions).filter_by(id=transaction_id).first()
        for key, value in kwargs.items():
            setattr(transaction, key, value)
        self.__db.save()
        return transaction

    def get_all_transactions_from_user(self, user_id):
        """Get all transactions from a user"""
        transactions = self.__db.query(Transactions).filter_by(sender_id=user_id).all()
        return transactions

    def get_all_transactions_to_user(self, user_id):
        """Get all transactions to the users table"""
        transactions = self.__db.query(Transactions).filter_by(receiver_id=user_id).all()
        return transactions
