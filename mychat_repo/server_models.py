import os
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class ClientContact(Base):
    """Связка контакт-клиент для хранения списка контактов"""
    # Название таблицы
    __tablename__ = 'ClientContact'
    # Первичный ключ
    ClientContactId = Column(Integer, primary_key=True)
    # id клиента
    ClientId = Column(Integer, ForeignKey('Client.ClientId'))
    # id контакта клиента
    ContactId = Column(Integer, ForeignKey('Client.ClientId'))

    def __init__(self, client_id, contact_id):
        self.ClientId = client_id
        self.ContactId = contact_id


class Client(Base):
    """Клиент"""
    # Название таблицы
    __tablename__ = 'Client'
    # Первичный ключ
    ClientId = Column(Integer, primary_key=True)
    # Имя клиента
    Name = Column(String, unique=True)
    # Информация не обязательное поле
    Info = Column(String, nullable=True)

    def __init__(self, name, info=None):
        self.Name = name
        if info:
            self.Info = info

    def __repr__(self):
        return "<Client ('%s')>" % self.Name

    def __eq__(self, other):
        # Клиенты равны если равны их имена
        return self.Name == other.Name


class ClientHistory(Base):
    """История клиента"""
    # Название таблицы
    __tablename__ = 'ClientHistory'
    # Первичный ключ
    ClientId = Column(Integer, primary_key=True)
    # ip-адрес
    IpAddr = Column(String, nullable=False)
    # Время входа
    LoginTime = Column(DateTime)

    def __init__(self, ip_addr, login_time):
        self.IpAddr = ip_addr
        self.LoginTime = login_time

    def __repr__(self):
        return "<Client {} was seen last time from {} at {}>".format(self.ClientId, self.IpAddr, self.IpAddr)


# путь до папки где лежит этот модуль
DB_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
# путь до файла базы данных
DB_PATH = os.path.join(DB_FOLDER_PATH, 'server.db')
# создаем движок
engine = create_engine('sqlite:///{}'.format(DB_PATH), echo=False)
# Не забываем создать структуру базы данных
Base.metadata.create_all(engine)
# Создаем сессию для работы
Session = sessionmaker(bind=engine)
session = Session()
# Рекомендуется брать 1 сессию и передавать параметром куда нам надо
session = session
