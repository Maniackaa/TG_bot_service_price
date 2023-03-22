from database.db import engine, User, Work
from sqlalchemy.orm import Session


def get_admin_id_from_username(username):
    with Session(engine) as session:
        user = session.query(User).filter(User.username == username).first()
        if user:
            print(user.tg_id, user)
            return user.tg_id
        else:
            print('Пользователь не найден')
# get_admin_id_from_username('AlexxxNik82')


def get_null_price_work_ids() -> list[int]:
    """Получить Список ID неоцененных работ"""
    with Session(engine) as session:
        works = session.query(Work).filter(Work.price == None).all()
        return [work.id for work in works]

# res = get_null_price_work_ids()
# print(res)


def get_works(tg_id):
    """Получение всех работ по ID"""
    try:
        with Session(engine) as session:
            print(tg_id)
            user = session.query(User).filter(User.tg_id == tg_id).first()
            if not user:
                raise ValueError('Такого пользователя нет')
            print(user)
            if user:
                all_work = f'Все работы пользователя {user.username}:\n\n'
                for work in user.works:
                    all_work += (
                        f'Авто: {work.auto}\n'
                        f'Работа: {work.name}\n'
                        f'Оценка: {work.price}\n\n')
                    print(f'Авто: {work.auto}\n'
                          f'Работа: {work.name}\n'
                          f'Оценка: {work.price}\n')
            else:
                all_work = f'У пользователя {user.username} нет работ:\n\n'
        print(all_work)
        return all_work
    except Exception as err:
        print('Не получилось')
        print(err)
        raise err


def get_work_from_id(work_id):
    """Получение работы по её ID"""
    with Session(engine) as session:
        works = session.query(Work).filter(Work.id == work_id).all()
        if works:
            work = works[0]
        else:
            return None
        return str(work)


def get_tg_id_from_work_id(work_id):
    """Получение tg ID по ID работы"""
    with Session(engine) as session:
        works = session.query(Work).filter(Work.id == work_id).all()
        if works:
            work = works[0]
        else:
            return None
        return work.user.tg_id


def get_works_on_period(start_date=None, end_date=None):
    """Получение всех работ"""
    try:
        with Session(engine) as session:
            works = session.query(Work).order_by(Work.id)
            all_work = 'Все работы :\n\n'
            sum_price = 0
            for work in works:
                all_work += (
                    f'Авто: {work.auto}\n'
                    f'Работа {work.id}: {work.name}\n'
                    f'Оценка: {work.price}\n\n')
                print(f'Авто: {work.auto}\n'
                      f'Работа {work.id}: {work.name}\n'
                      f'Оценка: {work.price}\n')
                if work.price:
                    sum_price += work.price
            all_work += f'Итоговая сумма: {sum_price}'
            print(all_work)

            return all_work
    except Exception as err:
        print('Не получилось')
        print(err)
        raise err
    return work

# w = get_work_from_id(2)
# print(w)

# res = get_tg_id_from_work_id(2)
# print(res)
