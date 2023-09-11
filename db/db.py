from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from os import getenv
from dotenv import load_dotenv
from models.user import Base


load_dotenv()


class DB:
    """
    DB class
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Constructor
        """

        user = getenv('MYSQL_USER')
        password = getenv('MYSQL_PWD')
        host = getenv('MYSQL_HOST')
        db_name = getenv('MYSQL_DB')
        env = getenv('APP_ENV')

        try:
            self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db_name}')
            self.reload()

            if env == 'test':
                Base.metadata.drop_all(self.__engine)
        except SQLAlchemyError as e:
            raise e


    def reload(self):
        """
        Reload
        """

        Base.metadata.create_all(self.__engine)
        session_maker = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_maker)



    def add(self, obj):
        """
        Add
        """

        self.__session.add(obj)

    def save(self):
        """
        Save
        """

        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete
        """

        if obj:
            self.__session.delete(obj)
