from database.db import engine, User
from sqlalchemy.orm import Session


def check_user(id):
    """Возвращает найденных пользователей по tg_id"""
    print('Ищем юзера', id)
    with Session(engine) as session:
        user = session.query(User).filter(User.tg_id == id).all()
        print(f'Результат: {user}')
        return user


def create_user(user):
    """Добавление пользователя в базу если его нет"""
    try:
        print('Берем данные с пользователя')
        print(user)
        tg_id = user.id
        print('tg_id', tg_id)
        username = user.username
        print('username', username)
        first_name = user.first_name
        print('first_name', first_name)
        last_name = user.last_name
        print('last_name', last_name)
        if check_user(tg_id):
            print('Пользователь есть в базе')
            return
        print('Добавляем пользователя')
        with Session(bind=engine) as session:
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


# 585896156
# get_works(585896156)
