from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter, Text, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from config_data.config import config
from database.read_db import get_null_price_work_ids, get_work_from_id, \
    get_tg_id_from_work_id, get_works_on_period
from database.write_db import db_update_price
from keyboards.keyboards import get_cost_kb, admin_start_kb


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.admin = config.tg_bot.admin

    async def __call__(self, message: Message) -> bool:
        print(f'Проверка на админа\n'
              f'{message}\n'
              f'{message.from_user.username} == {self.admin}\n'
              f'{message.from_user.username == self.admin}')
        return message.from_user.username == self.admin


admin_router = Router()
admin_router.message.filter(IsAdmin())


class FSMAdminMode(StatesGroup):
    change_price = State()


# Сброс состояния
@admin_router.message(Command(commands=["Отмена"]))
async def process_cancel_command(message: Message):
    print('Админская отмена')
    await message.answer('Сброс состояния',
                         reply_markup=admin_start_kb)


@admin_router.message(Command(commands=["Прислать_пустые"]))
async def process_start_command_admin(message: Message):
    null_price_work = get_null_price_work_ids()
    if null_price_work:
        for work_id in null_price_work:
            await message.answer(text=get_work_from_id(work_id),
                                 reply_markup=get_cost_kb(2))
    else:
        await message.answer(text='Нет неоцененных работ')


# Нажатие кнопки Скрыть
@admin_router.callback_query(Text(text=['close']))
async def process_button_press1(callback: CallbackQuery):
    print(f'Нажата {callback.message.message_id}')
    print('callback', callback.data)
    if callback.data == 'close':
        print('Удаляю')
        await callback.message.delete()


# Нажатие кнопки 'Указать стоимость'
@admin_router.callback_query(Text(text=['price']))
async def process_button_press2(callback: CallbackQuery, state: FSMContext):
    print("Мессадж:", callback.message)
    print(f'Нажата {callback.message.message_id}')
    print('callback', callback.data)
    work_id = callback.message.text.split()[0]
    print(work_id)
    print('Переход в состояние change_price')
    await state.set_state(FSMAdminMode.change_price)
    await state.update_data(work_id=work_id,
                            message_id=callback.message.message_id)
    print(state)
    await callback.message.reply(f'Введите оплату за работу № {work_id}')


# Внести цену
@admin_router.message(StateFilter(FSMAdminMode.change_price))
async def update_price(message: Message, state: FSMContext, bot: Bot):
    print('Внести цену')
    print(state)
    print(message)
    data = await state.get_data()
    work_id = data['work_id']
    price = message.text
    if price.isdigit():
        message_id = data['message_id']
        price = int(price)
        print('msg_id', message_id)
        worker_tg_id, work = db_update_price(work_id, price)
        # Удалить сообщение
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message_id)
        await state.clear()
        await message.answer(f'Стоимость обновлена\n\n{work}')
        work_user_tg_id = get_tg_id_from_work_id(work_id)
        await bot.send_message(text=f'Ваша работа оценена:\n\n{work}',
                               chat_id=work_user_tg_id)
    else:
        await message.answer(
            f'Вам необходимо ввести число для работы № {work_id}')


# Показать все работы
@admin_router.message(Command(commands=["Все_работы"]))
async def process_show_work_command(message: Message):
    text = get_works_on_period()
    print(len(text))
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await message.answer(text[x:x + 4096])
    else:
        await message.answer(text)
