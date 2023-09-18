from models.messages import Messages
from db.storage import DB

messages = Messages()

class MessagesService:
    __db = DB()
    __db.reload()

    def create_message(self, **kwargs):
        """Create message"""
        content = kwargs.get('content')
        sender_id = kwargs.get('sender_id')
        receiver_id = kwargs.get('receiver_id')
        message = Messages(content=content, sender_id=sender_id, receiver_id=receiver_id)
        self.__db.add(message)
        self.__db.save()
        return message

    def get_message(self, message_id):
        """Get message"""
        message = self.__db.query(Messages).filter_by(id=message_id).first()
        return message

    def get_specific_user_messages(self, user_id):
        """Get specific user messages"""
        messages = self.__db.query(Messages).filter_by(receiver_id=user_id).all()
        return messages

    def delete_message(self, message_id):
        """Delete message"""
        message = self.__db.query(Messages).filter_by(id=message_id).first()
        self.__db.delete(message)
        self.__db.save()
        return message

    def delete_all_user_messages(self, user_id):
        """Delete all user messages"""
        messages = self.__db.query(Messages).filter_by(receiver_id=user_id).all()
        for message in messages:
            self.__db.delete(message)
            self.__db.save()
        return messages
