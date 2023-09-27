from models.accounts import Accounts
from models.transactions import Transactions
from models.users import User
from db.storage import DB

class GetRelationships:
    """Get relationships"""
    __db = DB()

    def get_user_from_accounts(self, account_id):
        """Get the user from the accounts table"""
        user = self.__db.query(Accounts).filter_by(id=account_id).first()
        return user.user

    def get_account_from_user(self, user_id):
        """Get the account from the users table"""
        user = self.__db.query(User).filter_by(id=user_id).first()
        return user.accounts


    def get_user_from_transactions(self, transaction_id):
        """Get the user from the transactions table"""
        transaction = self.__db.query(Transactions).filter_by(id=transaction_id).first()
        return transaction.sender


    def get_user_from_account_number(self, account_number):
        """Get the user from the accounts table"""
        account = self.__db.query(Accounts).filter_by(account_number=account_number).first()
        return account.user

