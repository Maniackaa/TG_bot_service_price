from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,\
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

kb = [
    [KeyboardButton(text="/Добавить_работу_на_оценку")],
    [KeyboardButton(text="/Мои_работы")]
    ]

start_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=kb,
                                                    resize_keyboard=True)
admin_kb = [
    [KeyboardButton(text="/Прислать_пустые")],
    [KeyboardButton(text="/Отмена")]
    ]
admin_start_kb = ReplyKeyboardMarkup(keyboard=admin_kb,
                                     resize_keyboard=True)


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
