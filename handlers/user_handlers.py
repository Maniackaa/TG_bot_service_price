from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter, Text, BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.types import CallbackQuery, Message

from database.read_db import get_works, get_admin_id_from_username, \
    get_work_from_id
from database.write_db import add_work_to_base
from keyboards.keyboards import q_kb, start_kb, get_cost_kb, admin_start_kb
from services.services import create_user


from config_data.config import config

router: Router = Router()


class IsAdmin(BaseFilter):
    """Фильтр на админа"""
    def __init__(self) -> None:
        self.admin = config.tg_bot.admin

    async def __call__(self, message: Message) -> bool:
        print(f'Проверка на админа\n'
              f'{message}\n'
              f'{message.from_user.username} == {self.admin}\n'
              f'{message.from_user.username == self.admin}')
        return message.from_user.username == self.admin


def is_admin(username):
    """Проверка на админа"""
    return username == config.tg_bot.admin


class FSMWorkAnket(StatesGroup):
    get_auto = State()
    get_work = State()
    add_work_again = State()
    appeal = State()


@router.message(Command(commands=["start"]))
async def process_start_command(message: Message, state: FSMContext):
    """Действие на команду /start"""
    await state.clear()
    user = message.from_user
    create_user(user)
    print('admin - ', is_admin(message.from_user.username))
    if is_admin(message.from_user.username):
        kb = admin_start_kb
    else:
        kb = start_kb
    await message.answer(f'Здравствуйте! {user.full_name} "{user.username}"',
                         reply_markup=kb)


# Сброс состояния
@router.message(Command(commands=["Отмена"]))
async def process_cancel_command(message: Message, state: FSMContext):
    """Действие на команду /Отмена"""
    print('Юзеровская отмена')
    await state.clear()
    await message.answer('Сброс состояния',
                         reply_markup=start_kb)


# Показать мои работы
@router.message(Command(commands=["Мои_работы"]), StateFilter(default_state))
async def process_show_work_command(message: Message):
    """Действие на команду /Мои_работы"""
    user = message.from_user.id
    text = get_works(user)
    print(len(text))
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await message.answer(text[x:x + 4096])
    else:
        await message.answer(text)


# Кнопка Добавление работы
@router.message(Command(commands=["Добавить_работу_на_оценку"]))
async def process_add_command(message: Message, state: FSMContext):
    """Действие на команду /Добавить_работу_на_оценку"""
    await message.answer('Введите Авто')
    await state.set_state(FSMWorkAnket.get_auto)


# Добавление авто
@router.message(StateFilter(FSMWorkAnket.get_auto), ~Text(startswith='/'))
async def process_auto(message: Message, state: FSMContext):
    """Режим после Добавить_работу_на_оценку
    Ввод авто"""
    input_text = message.text
    if len(input_text) > 5:
        await state.update_data(auto=message.text)
        await message.answer(f'Марка авто: {message.text}'
                             f'\nВведите описание работы')
        await state.set_state(FSMWorkAnket.get_work)
    else:
        await message.answer('Не похоже на авто')


# Добавление имени работы
@router.message(StateFilter(FSMWorkAnket.get_work), ~Text(startswith='/'))
async def process_work(message: Message, state: FSMContext):
    """Режим после Добавить_работу_на_оценку, Ввод авто
    Ввод имени работы"""
    input_text = message.text
    if len(input_text) > 5:
        await state.update_data(work_name=message.text)
        await message.answer(f'Описание работы:\n{message.text}\n'
                             f'\nВсё верно?":\n',
                             reply_markup=q_kb)
        await state.set_state(FSMWorkAnket.add_work_again)
    else:
        await message.answer('Не похоже на название работы')


# Обработка вопроса продолжить или нет
@router.callback_query(StateFilter(FSMWorkAnket.add_work_again))
async def process_q(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """Режим после Добавить_работу_на_оценку, Ввод авто, Ввод имени работы
    Обработка вопроса Сохранить/отменить"""
    tg_id = callback.from_user.id
    await callback.message.edit_text(text=f'Вы выбрали {callback.data}')

    if callback.data == 'Отмена':
        await state.set_state(default_state)

    if callback.data == 'Сохранить':
        await state.set_state(default_state)
        print('Сохраняем результат')
        data = await state.get_data()
        auto = data['auto']
        work_name = data['work_name']
        work = add_work_to_base(tg_id, auto, work_name)
        if work:
            await callback.message.answer(f'Успешно сохранено\n\n{work}',
                                          reply_markup=start_kb)

            # Отправка работы админу:
            try:
                await bot.send_message(
                    chat_id=get_admin_id_from_username(config.tg_bot.admin),
                    text=work,
                    reply_markup=get_cost_kb(2))
                await callback.message.answer(
                    'Ваша работа отправлена на оценку.',
                    reply_markup=start_kb)
            except Exception as err:
                print('Произошла ошибка при отправке работы.'
                      ' Сообщите администратору', err)
                await callback.message.answer(
                    'Произошла ошибка при отправке работы.'
                    ' Сообщите администратору',
                    reply_markup=start_kb)
        else:
            await callback.message.answer(
                'Произошла ошибка при сохранении работы',
                reply_markup=start_kb)
            print('Произошла ошибка при сохранении работы')


# Действие на нажатие кнопки Подтвердить
@router.callback_query(Text(startswith='user_price_confirm'))
async def user_price_confirm(callback: CallbackQuery):
    """Действие на нажатие Сохранить"""
    print('callback', callback.data)
    print('Удаляю')
    await callback.message.edit_text(callback.message.text + ' (подтверждено)', reply_markup=None)


# ******* Обжалование работы ********

# Действие на нажатие кнопки Обжаловать
@router.callback_query(Text(startswith='user_price_appeal'))
async def user_price_appeal(callback: CallbackQuery,
                            state: FSMContext, bot: Bot):
    """Действие на нажатие Сохранить"""
    print('callback', callback.data)
    await state.set_state(FSMWorkAnket.appeal)
    work_id = callback.message.text.split()[0]
    await state.update_data(work_id=work_id)
    await state.update_data(message_id=callback.message.message_id)
    await callback.message.answer('Добавьте комментарий к обжалованию')


# Добавление комментария при обжаловании
@router.message(StateFilter(FSMWorkAnket.appeal))
async def appeal_comment(message: Message, state: FSMContext, bot: Bot):
    """Действие после Сохранить
    Добавление комментария"""
    comment = message.text
    if len(comment) < 5:
        await message.answer('Комментарий не может быть пустым')
    else:
        # Повторная отправка на переоценку
        try:
            data = await state.get_data()
            work_id = data.get('work_id')
            work = get_work_from_id(work_id)
            print('ОТправляем работу на переоценку\n', work)
            await bot.send_message(
                chat_id=get_admin_id_from_username(config.tg_bot.admin),
                text=(f'Работа прислана на переоценку со'
                      f' следующим комментарием:\n'
                      f'{comment}'))
            await bot.send_message(
                chat_id=get_admin_id_from_username(config.tg_bot.admin),
                text=work,
                reply_markup=get_cost_kb(2))
            await message.answer(
                'Ваша работа отправлена на переценку.',
                reply_markup=start_kb)
            # Скроем сообщение, которое обжаловали
            msg_to_del = data.get('message_id')
            print('Удаляем сообщение', msg_to_del)
            await bot.delete_message(chat_id=message.from_user.id,
                                     message_id=msg_to_del)
        except Exception as err:
            print('Произошла ошибка при отправке работы.'
                  ' Сообщите администратору', err)
            await message.answer(
                'Произошла ошибка при отправке работы.'
                ' Сообщите администратору',
                reply_markup=start_kb)


# Последний фильтр
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    """Если не один фильтр не сработал"""
    print('Эхо')
    await message.answer(text='Неизвестная команда')
