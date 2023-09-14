from models.users import User
from uuid import uuid4
from db import storage
from bcrypt import hashpw, gensalt, checkpw

class UserAuth:
    _db = storage



    def hash_password(self, password):
        password_bytes = password.encode('utf-8')
        return hashpw(password_bytes, gensalt())

    def verify_password(self, password, hashed_password):
        return checkpw(password, hashed_password)

    def create_user(self, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        phone_number = kwargs.get('phone_number')
        location = kwargs.get('location')
        is_superuser = kwargs.get('is_superuser')
        is_active = kwargs.get('is_active')
        login_time = kwargs.get('last_login')
        password = self.hash_password(password)
        user = User(email=email, password=password, first_name=first_name, last_name=last_name, phone_number=phone_number, location=location, is_superuser=is_superuser, is_active=is_active, last_login=login_time)
        storage.reload()
        self._db.add(user)
        self._db.save()
        return user

    def get_user_by_email(self, email):
        try:
            return self._db.query.filter_by(email=email).first()
        except Exception as e:
            return None

    def get_user_by_id(self, id):
        try:
            return self._db.query.filter_by(id=id).first()
        except Exception as e:
            return None

    def get_all_users(self):
        return self._db.query.all()

    def delete_user(self, id):
        user = self.get_user_by_id(id)
        self._db.delete(user)
        self._db.save()
        return True

    def update_user(self, id, email, password):
        try:
            user = self.get_user_by_id(id)
            if user:
                if email:
                    user.email = email
                if password:
                    user.password = self.hash_password(password)
                self._db.save()
                return user
            return None
        except Exception as e:
            return None
