from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from db import Group


def menu_button(admin=False):
    kb = ReplyKeyboardBuilder()
    if admin is True:
        kb.add(*[KeyboardButton(text='📊 Statistika 📊'),
                 KeyboardButton(text='⚙️ Settings ⚙️')])
    else:
        kb.add(*[KeyboardButton(text='📒 Mening natijam 📒')])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def settings_btn():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text='👥 Group 👥'),
             KeyboardButton(text='◀️ Ortga')])
    return kb.as_markup(resize_keyboard=True)


async def confirm():
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text='✅Ha', callback_data='yes'),
            InlineKeyboardButton(text='❌ Qayta o\'tish', callback_data='no'))
    ikb.adjust(2)
    return ikb.as_markup()
