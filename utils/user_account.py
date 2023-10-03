from models.accounts import Accounts
from models.transactions import Transactions
from db.storage import DB
import random
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError


class AccountService:
    __db = DB()
    __db.reload()


    def create_account_number(self):
        """Create account number"""
        account_number = str(random.randint(10*9, 10**10-1))
        return account_number

    def get_user_id_from_account_number(self, account_number):
        """Get user id from account number"""
        account = self.__db.query(Accounts).filter_by(account_number=account_number).first()
        return account.user_id

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

    def get_account_by_user_id(self, user_id):
        """get account numebr by user id"""
        account = self.__db.query(Accounts).filter_by(user_id=user_id).first()
        return account.account_number

    def add_total_funds(self, account_number, amount):
        """Add total funds"""
        account = self.__db.query(Accounts).filter_by(account_number=account_number).first()
        account.Total_funds += amount
        self.__db.save()
        return account

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
                self._db.begin()
                sender_account.Total_funds -= amount
                sender_account.outgoing_funds += amount
                receiver_account.incoming_funds += amount
                self._db.save()

            except SQLAlchemyError as e:
                self._db.rollback()
                return jsonify({"message": "Transaction failed"}), 400
        else:
            return jsonify({"message": "The sender_account or receiver account does not exist"}), 400

        return jsonify({"message": "Transaction successful"}), 200

    def reverse_money(self, amount, sender_id, receiver_id):
        sender_account = self.__db.query(Accounts).filter_by(user_id=sender_id).first()
        receiver_account = self._db.query(Accounts).filter_by(user_id=receiver_id).first()
        if sender_account and receiver_account:
            try:
                self._db.begin()
                sender_account.outgoing_funds -= amount
                sender_account.Total_funds += amount
                receiver_account.incoming_funds -= amount
                self.__db.save()

            except SQLAlchemyError as e:
                self.__db.rollback()
                return jsonify({"message": "reversal failed"})
        else:
            return jsonify({"message": "the sender or the receiver does not exist"}), 400
        return jsonify({"message": "amount successfully reversed"})


    def send_money(self, amount, sender_id, receiver_id):

        sender_account = self.__db.query(Accounts).filter_by(user_id=sender_id).first()
        receiver_account = self._db.query(Accounts).filter_by(user_id=receiver_id).first()
        if sender_account and receiver_account:
            try:
                self._db.begin()
                sender_account.outgoing_funds -= amount
                receiver_account.Total_funds += amount
                receiver_account.incoming_funds -= amount
                self.__db.save()

            except SQLAlchemyError as e:
                self.__db.rollback()
                return jsonify({"message": "approval failed"})
        else:
            return jsonify({"message": "the sender or the receiver does not exist"}), 400
        return jsonify({"message": "amount successfully sent"})


    def create_conflict(self, transaction_id):
        # take the transaction id
        transaction = self.__db.query(Transactions).filter_by(id=transaction_id).first()
        if transaction:
            # if the transaction exixts set the status of that transaction to true
            transaction.conflict = "True"
            self.__db.save()
        else:
            return jsonify({"message": "such a transaction does not exist"})
        return jsonify({"message": "money locked until conflict is resolved"})
