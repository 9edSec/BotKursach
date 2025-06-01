import json

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
)

from aiogram.utils.keyboard import ReplyKeyboardBuilder, \
    InlineKeyboardBuilder


from bot.tools.tool import UserTool


msg = UserTool()

# Reply Клавиатура (Получить сертификат, Частые вопросы)
def kb_start():
    kb = ReplyKeyboardBuilder()

    kb.button(
        text=msg.user_keyboard['kb_start']['get_certificate']
    )

    kb.button(
        text=msg.user_keyboard['kb_start']['faq']
    )
    return kb.adjust(1,1).as_markup(resize_keyboard=True)


def kb_get_certificate():
    kb = InlineKeyboardBuilder()

    kb.button(
        text=msg.user_keyboard['kb_get_certificate']['study_materials'], web_app=WebAppInfo(url="https://pressf-school.ru")
    )

    kb.button(
        text=msg.user_keyboard['kb_get_certificate']['take_the_test'], callback_data='take_test'
    )
    return kb.adjust(1,1).as_markup()

check_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проверить ответы', callback_data="check_answers")]
])

restart_test_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Решить заново', callback_data='take_test')]
])

get_certificate_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получить сертификат!', callback_data="get_certificate")]
])

reply_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Написать', callback_data="reply_to_user", url="https://t.me/spectr_inc")]
])

no_response = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Нет ответа?', callback_data='no_to_respone')]
])