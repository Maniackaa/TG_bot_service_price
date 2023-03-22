from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,\
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

kb = [
    [KeyboardButton(text="/Добавить_работу_на_оценку")],
    [KeyboardButton(text="/Мои_работы")],
    [KeyboardButton(text="/Отмена")]
    ]

start_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=kb,
                                                    resize_keyboard=True)
admin_kb = [
    [KeyboardButton(text="/Прислать_пустые")],
    # [KeyboardButton(text="/Все_работы")],
    [KeyboardButton(text="/Работы_за_этот_месяц")],
    [KeyboardButton(text="/Работы_за_прошлый_месяц")],
    [KeyboardButton(text="/Отмена")]
    ]
admin_start_kb = ReplyKeyboardMarkup(keyboard=admin_kb,
                                     resize_keyboard=True)


def get_inline_kb(width: int, buttons: list) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()


user_price_confirm_buttons = [
    InlineKeyboardButton(
        text='Подтвердить',
        callback_data='user_price_confirm'),
    InlineKeyboardButton(
        text='Обжаловать цену',
        callback_data='user_price_appeal')]

user_price_confirm_kb = get_inline_kb(2, user_price_confirm_buttons)


def question_kb(width: int) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    buttons = [
        # InlineKeyboardButton(
        # text='Добавить еще работу',
        # callback_data='Добавить еще работу'),
        InlineKeyboardButton(
            text='Сохранить',
            callback_data='Сохранить'),
        InlineKeyboardButton(
            text='Отмена',
            callback_data='Отмена')]
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()


def get_cost_kb(width: int, price=None) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    if price:
        price_text = f'{price} Изменить'
    else:
        price_text = 'Указать стоимость'

    buttons = [
        InlineKeyboardButton(text=price_text,
                             callback_data='price'),

        InlineKeyboardButton(text='Скрыть',
                             callback_data='close')]
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()


q_kb = question_kb(2)
