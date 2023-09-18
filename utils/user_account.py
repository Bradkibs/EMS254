from models.accounts import Accounts
from db.storage import DB
import random
from flask import jsonify



class AccountService:
    __db = DB()
    __db.reload()


    def create_account_number(self):
        """Create account number"""
        account_number = str(random.randint(10*9, 10**10-1))
        return account_number

    def create_account(self, **kwargs):
        """Create account"""
        account_number = self.create_account_number()
        # check if account number exists
        account_exists = self.__db.query(Accounts).filter_by(account_number=account_number).first()
        if account_exists:
            while account_exists:
                account_number = self.create_account_number()
        Total_funds = kwargs.get('Total_funds')
        incomming_funds = kwargs.get('incomming_funds')
        outgoing_funds = kwargs.get('outgoing_funds')
        user_id = kwargs.get('user_id')
        account = Accounts(account_number=account_number, Total_funds=Total_funds, incomming_funds=incomming_funds, outgoing_funds=outgoing_funds, user_id=user_id)
        self.__db.add(account)
        self.__db.save()
        return account

    def get_account(self, account_number):
        """Get account"""
        account = self.__db.query(Accounts).filter_by(account_number=account_number).first()
        return account

    def add_total_funds(self, account_number, amount):
        """Add total funds"""
        account = self.__db.query(Accounts).filter_by(account_number=account_number).first()
        account.Total_funds += amount
        self.__db.save()
        return account

    # def add_incomming_funds(self, account_number, amount):
    #     """Add incomming funds to the incomming funds"""
    #     account = self.__db.query(Accounts).filter_by(account_number=account_number).first()
    #     account.incomming_funds += amount
    #     self.__db.save()
    #     return account

    # def add_outgoing_funds(self, account_number, amount):
    #     """Add outgoing funds to the outgoing funds"""
    #     account = self.__db.query(Accounts).filter_by(account_number=account_number).first()
    #     account.outgoing_funds += amount
    #     self.__db.save()
    #     return account

    # def subtract_outgoing_funds(self, account_number, amount):
    #     """Subtract outgoing funds from total funds"""
    #     account = self.__db.query(Accounts).filter_by(account_number=account_number).first()
    #     account.total -= amount
    #     account.outgoing_funds = amount
    #     self.__db.save()
    #     return account

    # def add_incoming_funds_to_total(self, account_number):
    #     """Add incoming funds to total funds"""
    #     account = self.__db.query(Accounts).filter_by(account_number=account_number).first()
    #     account.total += account.incoming_funds
    #     account.incoming_funds = 0
    #     self.__db.save()
    #     return account

    def transact(self, amount, sender_id, receiver_id):
        """ creating a sql transaction"""
        if not amount and amount < 100:
            return jsonify({"message": "Amount must be greater than 100"}), 400
        if not sender_id:
            return jsonify({"message": "Sender id is required"}), 400
        if not receiver_id:
            return jsonify({"message": "Receiver id is required"}), 400
        sender_account = self.__db.query(Accounts).filter_by(user_id=sender_id).first()
        receiver_account = self.__db.query(Accounts).filter_by(user_id=receiver_id).first()

        if sender_account and receiver_account:
            if sender_account.Total_funds < amount:
                return jsonify({"message": "Insufficient funds"}), 400
            try:
                _db.begin()
                sender_account.Total_funds -= amount
                sender_account.outgoing_funds += amount
                receiver_account.incoming_funds +=  amount
                _db.save()
            except Exception as e:
                _db.rollback()
                return jsonify({"message": "Transaction failed"}), 400
        else:
            return jsonify({"message": "The sender_account or receiver account does not exist"}), 400

        return jsonify({"message": "Transaction successful"}), 200
