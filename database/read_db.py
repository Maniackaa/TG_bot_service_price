from collections import Counter
from datetime import datetime

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


def get_report(works: list[Work]):
    price_counter = Counter()
    num_counter = Counter()
    uncost_counter = Counter()
    total_counter = Counter()
    users = set()
    for work in works:
        num_counter.update({work.user: 1})
        total_counter.update({'total_sum': work.price or 0})
        if work.price:
            price_counter.update({work.user: work.price or 0})
        else:
            uncost_counter.update({work.user: 1})
        users.add(work.user)
    print(price_counter)
    print(num_counter)
    print(uncost_counter)
    print(users)
    report = '\n<b>Сводный итог:</b>\n\n'
    for user in users:
        report += (f'<b>{user}</b> ({num_counter.get(user)})\n')
        report += (f'Общая сумма: {price_counter.get(user)}\n'
                   f'Работ без оценки: {uncost_counter.get(user) or 0}\n\n')
    report += f'Итоговая сумма: {total_counter.get("total_sum"):n}'
    return report


def get_works_on_period(start_date=datetime(2023, 1, 1),
                        end_date=datetime.now()):
    """Получение всех работ"""
    try:
        with Session(engine) as session:
            works = session.query(Work).order_by(Work.id).filter(
                Work.datetime <= end_date, Work.datetime > start_date).all()
            all_work = (f'<b>Все работы за\n'
                        f'{start_date.strftime("%d %B %Y")} - '
                        f'{end_date.strftime("%d %B %Y")}:</b>\n\n')
            sum_price = 0
            for work in works:
                all_work += (
                    f'Дата: {work.datetime[:16]}\n'
                    f'Авто: {work.auto}\n'
                    f'Работа {work.id}: {work.name}\n'
                    f'Оценка: {work.price}\n\n')
                # print(f'Авто: {work.auto}\n'
                #       f'Работа {work.id}: {work.name}\n'
                #       f'Оценка: {work.price}\n')
                if work.price:
                    sum_price += work.price
            all_work += get_report(works)
            # print(all_work)
            print('Всего', len(works))

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


# get_works_on_period(start_date=datetime(2023, 3, 22, 18))
# get_works_on_period()
