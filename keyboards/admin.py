from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils import db

bank_admin_data = CallbackData("bank_admin", "id")
bank_data = CallbackData("bank", "id")

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton("Изменить поставщика"),
                                                                  KeyboardButton("Банки"),
                                                                  KeyboardButton("Создать договор"))

accept_new_provider = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("Обновить", callback_data="new_provider_accept"),
    InlineKeyboardButton("Отмена", callback_data="new_provider_cancel"))

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))


def get_banks_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    banks = db.get_banks()
    for bank in banks:
        kb.add(InlineKeyboardButton(bank["name"], callback_data=bank_admin_data.new(bank["id"])))
    kb.add(InlineKeyboardButton("Добавить банк", callback_data="add_bank"))
    return kb


def get_banks():
    kb = InlineKeyboardMarkup(row_width=1)
    banks = db.get_banks()
    for bank in banks:
        kb.add(InlineKeyboardButton(bank["name"], callback_data=bank_data.new(bank["id"])))
    return kb
