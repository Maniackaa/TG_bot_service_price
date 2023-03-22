from sqlalchemy import select

from database.db import engine, User, Work
from sqlalchemy.orm import Session


def check_user(id):
    print('Ищем юзера', id)
    with Session(engine) as session:
        user = session.query(User).filter(User.tg_id == id).all()
        print(f'Результат: {user}')
        return user


def create_user(tg_id, username, first_name, last_name):
    try:
        if check_user(tg_id):
            print('Пользователь есть в базе')
            return
        print('Добавляем пользователя')
        with Session(engine) as session:
            new_user = User(tg_id=tg_id,
                            username=username,
                            first_name=first_name,
                            last_name=last_name)

            session.add(new_user)
            session.commit()
            print(f'Пользователь создан: {new_user}')

    except Exception as err:
        print('Пользователь не создан')
        print(err)
        raise err


def add_work_to_base(tg_id, auto, workname):
    print('Сохраняем в базу', tg_id, auto, workname)
    try:
        with Session(engine) as session:
            user = session.query(User).filter(User.tg_id == tg_id).first()
            print('Юзер:', user)
            work = Work(auto=auto, user=user, name=workname)
            session.add(work)
            session.commit()
            print('Работа добавлена')

    except Exception as err:
        print('Не получилось сохранить работу')
        print(err)
        raise err


create_user(585896156, 'AlexxxNik82', None, None)
print('-----------')
add_work_to_base(585896156, 'Автомобиль 1',
                 "Немного не понятно как работают хэндлеры.")


def get_test_work():

    with Session(engine) as session:
        work: Work = session.execute(
            select(Work).order_by(Work.id)).fetchone()[0]
        print(work)
        return work


# print('-----------')
# print('Достаем работу')
# w = get_test_work()
# print(w)
# print(type(w))
# print(w)
#


def get_works_on_period(start_date=None, end_date=None):
    """Получение всех работ"""

    with Session(engine) as session:
        work = session.query(Work).order_by(Work.id).first()
        print(work)

    return work


get_works_on_period()
