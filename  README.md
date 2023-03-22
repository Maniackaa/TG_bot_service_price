## Бот для отправки работ и их оценки

### Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Maniackaa/TG_bot_service_price.git
```



Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
venv/Script/activate
```

Установить зависимости из файла req.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r req.txt
```

Создать файл **myenv.env** в корне проекта.
Содержимое файла:
```
BOT_TOKEN='Вставить токен бота'
ADMIN_USERNAME='Username админа'
DB_PATH='Имя базы данных.sqlite3'  
```
Пример файла:
```
BOT_TOKEN='6123456789:AAHBkQm4xGCJ3oSTfvvcHg7213fa'
ADMIN_USERNAME='AlexxxNik82'
DB_PATH='db.sqlite3'
```

Запустить проект:

```
python bot.py

или через ярлык Запуск.cmd
```



2023 ©️Team №18 

