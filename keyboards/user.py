from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

days_data = CallbackData("day", "weekday", "is_include")

weekdays = [{0: "Понедельник", 1: "✅ Понедельник"}, {0: "Вторник", 1: "✅ Вторник"},
            {0: "Среда", 1: "✅ Среда"}, {0: "Четверг", 1: "✅ Четверг"},
            {0: "Пятница", 1: "✅ Пятница"}, {0: "Суббота", 1: "✅ Суббота"},
            {0: "Воскресенье", 1: "✅ Воскресенье"}]

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(KeyboardButton("Создать договор"))

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))

days = InlineKeyboardMarkup(row_width=1)
for i in range(7):
    days.add(InlineKeyboardButton(weekdays[i][0], callback_data=days_data.new(i, 0)))

days_count = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton("1", callback_data="days_count:1"),
                                                   InlineKeyboardButton("2", callback_data="days_count:2"))


def get_days(days_info):
    kb = InlineKeyboardMarkup(row_width=1)
    print(days_info)
    for i in range(7):
        kb.add(InlineKeyboardButton(weekdays[i][days_info[i]],
                                    callback_data=days_data.new(i, days_info[i])))
    kb.add(InlineKeyboardButton("Продолжить", callback_data="days_finish"))
    return kb
