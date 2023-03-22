from dataclasses import dataclass
from environs import Env
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR.parent / 'bot_django'


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_port: str
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных
    db_path: str  # путь к файлу


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота
    admin: str  # Логин администратора
    base_dir = BASE_DIR
    media_dir = MEDIA_DIR


@dataclass
class GoogleTables:
    table_url: str


@dataclass
class Config:
    tg_bot: TgBot
    g_tables: GoogleTables
    db: DatabaseConfig


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            admin=env('ADMIN_USERNAME')
            ),
        g_tables=GoogleTables(table_url=env('TABLE_URL')),
        db=DatabaseConfig(
            database=env('DB_NAME'),
            db_host=env('DB_HOST'),
            db_port=env('DB_PORT'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD'),
            db_path=BASE_DIR / env('DB_PATH'))
            )


config = load_config('myenv.env')

# print(config.db)
