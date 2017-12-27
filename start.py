# Служебный скрипт запуска/останова нескольких клиентских приложений
import os
from subprocess import Popen, CREATE_NEW_CONSOLE
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# путь к базе данных
db_dir = os.path.abspath(os.curdir)
db_path = str(db_dir) + '\\messenger_db.db'

# проверяю существует ли база данных в директории и если нет, то создаю её
if os.path.isfile(db_path):
    pass
else:
    engine = create_engine('sqlite:///messenger_db.db', echo=False)
    Base = declarative_base()
    Base.metadata.create_all(engine)

# список запущенных процессов
p_list = []

while True:
    user = input("Запустить сервер и клиентов (s) / Выйти (q)")

    if user == 's':
        # запускаем сервер
        # Запускаем серверный скрипт и добавляем его в список процессов
        p_list.append(Popen('python server.py',
                            creationflags=CREATE_NEW_CONSOLE))
        print('Сервер запущен')
        # ждем на всякий пожарный
        time.sleep(1)
        # запускаем клиентов на чтение
        for _ in range(3):
            # Запускаем клиентский скрипт и добавляем его в список процессов
            p_list.append(Popen('python client.py localhost 7777 r',
                                creationflags=CREATE_NEW_CONSOLE))
        print('Клиенты на чтение запущены')
        # запускаем клиента на запись случайное число
        for _ in range(2):
            # Запускаем клиентский скрипт и добавляем его в список процессов
            p_list.append(Popen('python client.py localhost 7777 w',
                                creationflags=CREATE_NEW_CONSOLE))
        print('Клиенты на запись запущены')
    elif user == 'q':
        print('Открыто процессов {}'.format(len(p_list)))
        for p in p_list:
            print('Закрываю {}'.format(p))
            p.kill()
        p_list.clear()
        print('Выхожу')
        break
