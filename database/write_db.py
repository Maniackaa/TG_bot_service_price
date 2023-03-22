from database.db import engine, User, Work
from sqlalchemy.orm import Session


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
            return str(work)
    except Exception as err:
        print('Не получилось сохранить работу')
        print(err)
        raise err


def db_update_price(work_id, price):
    """Обновить цену работы"""
    print('update_price', work_id, price)
    with Session(engine) as session:
        work = session.query(Work).filter(Work.id == work_id).first()
        work.price = price
        session.commit()
        print(work)
        return (work.user.tg_id, str(work))
