from datetime import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


from config_data.config import config

engine = create_engine(f"sqlite:///{config.db.db_path}", echo=False)
connection = engine.connect()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'telegram_user'

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    comment='Первичный ключ')
    tg_id: Mapped[str] = mapped_column(unique=True,
                                       comment='id Tg',
                                       nullable=False)
    added: Mapped[str] = mapped_column(default=datetime.now())
    username: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    surname: Mapped[str] = mapped_column(nullable=True)
    middle_name: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(default='user')
    works: Mapped[list['Work']] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return str(f'{self.username}')


class Work(Base):

    __tablename__ = 'work'
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment='Первичный ключ')
    datetime: Mapped[str] = mapped_column(default=datetime.now())
    auto: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("telegram_user.id"))
    user: Mapped['User'] = relationship(back_populates='works')

    def __repr__(self) -> str:
        return (f'{self.id} {self.user} {self.datetime[:16]}\n\n'
                f'<b>Авто:</b> {self.auto}\n\n'
                f'<b>Работа</b>:\n'
                f'{self.name}\n\n'
                f'<b>Оплата</b>: {self.price}')


Base.metadata.create_all(engine)
