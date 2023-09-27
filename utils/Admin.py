from models.accounts import Accounts
from models.transactions import Transactions
from models.users import User
from db.storage import DB

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
