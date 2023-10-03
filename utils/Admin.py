from models.accounts import Accounts
from models.transactions import Transactions
from models.users import User
from db.storage import DB
from flask import jsonify

class Admin:

    db = DB()

    def get_all_transactions(self):
        """Get all transactions
        for admin purposes"""
        transactions = self.__db.query(Transactions).all()
        return transactions

    def get_all_accounts(self):
        """Get all accounts
        for admin purposes"""
        accounts = self.__db.query(Accounts).all()
        return accounts

    def get_all_users(self):
        """Get all users
        for admin purposes"""
        users = self.__db.query(User).all()
        return users

    def resolve_conflicts(self, transaction_id):
        transaction = self.__db.query(Transactions).filter_by(id=transaction_id).first()
        if transaction:
            transaction.conflict = "False"
            self.__db.save()
        else:
            return jsonify({"message": "Transaction not found"})
        return jsonify({"message": "conflict resolved by admin"})


    # admin has the right to return the money
    # sender completes transaction and sends the monet
