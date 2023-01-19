from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils import db
from utils import api

teach_faculties_data = CallbackData("select_fac_teach", "fac_id")
faculties_data = CallbackData("select_fac", "fac_id")
subfaculties_data = CallbackData("select_subfac", "fac_id", "subfac_id")
teach_data = CallbackData("select_teach", "teach_id")
course_data = CallbackData("select_course", "fac_id", "course")
group_data = CallbackData("select_group", "group_id")

menu_kb = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(KeyboardButton('Расписание на сегодня'),
                                                                     KeyboardButton('Расписание на завтра'),
                                                                     KeyboardButton('Выбрать дату'),
                                                                     KeyboardButton('Экзамены'))

change_kb = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("🔄Изменить группу", callback_data="change_group"))

user_type = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton("Я студент", callback_data="type:1"),
                                                  InlineKeyboardButton("Я преподаватель", callback_data="type:2"))


def get_menu_kb(chat_type):
    if chat_type in ["group", "supergroup"]:
        return None
    return menu_kb


def get_faculties():
    kb = InlineKeyboardMarkup(row_width=3)
    faculties = api.get_faculties()
    for faculty in faculties:
        in_button = InlineKeyboardButton(faculty["shortTitle"], callback_data=faculties_data.new(faculty["id"]))
        kb.insert(in_button)
    return kb


def get_faculties_for_teacher():
    kb = InlineKeyboardMarkup(row_width=3)
    faculties = api.get_faculties()
    for faculty in faculties:
        in_button = InlineKeyboardButton(faculty["shortTitle"], callback_data=teach_faculties_data.new(faculty["id"]))
        kb.insert(in_button)
    return kb


def get_subfacltiues(fac_id):
    kb = InlineKeyboardMarkup(row_width=3)
    subfaculties = api.get_subfaculties(fac_id)
    for subfaculty in subfaculties:
        in_button = InlineKeyboardButton(subfaculty["shortTitle"],
                                         callback_data=subfaculties_data.new(fac_id, subfaculty["id"]))
        kb.insert(in_button)
    return kb


def get_teachers(fac_id, subfac_id):
    kb = InlineKeyboardMarkup(row_width=3)
    teachers = api.get_teachers(fac_id, subfac_id)
    for teacher in teachers:
        fullname = f'{teacher["lastName"]} {teacher["firstName"][0]}.{teacher["parentName"][0]}.'
        in_button = InlineKeyboardButton(fullname,
                                         callback_data=teach_data.new(teacher["id"]))
        kb.insert(in_button)
    return kb


def get_courses(fac_id):
    kb = InlineKeyboardMarkup(row_width=6)
    courses = api.get_courses(fac_id)
    courses_emoji = ["", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for course in courses:
        in_button = InlineKeyboardButton(courses_emoji[int(course["course"])],
                                         callback_data=course_data.new(fac_id, int(course["course"])))
        kb.insert(in_button)
    return kb


def get_groups(fac_id, course):
    kb = InlineKeyboardMarkup(row_width=3)
    groups = api.get_groups(fac_id, course)
    for group in groups:
        in_button = InlineKeyboardButton(group["title"], callback_data=group_data.new(group["id"]))
        kb.insert(in_button)
    return kb
