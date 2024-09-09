from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


#start_kb
button_docs = InlineKeyboardButton(text="📄Документы", callback_data="docs_start")
button_front = InlineKeyboardButton(text="🪖На фронт", callback_data="front_start")

start_kb = InlineKeyboardMarkup(inline_keyboard=[[button_docs, button_front]])

button_menu = KeyboardButton(text="В меню")
menu_kb = ReplyKeyboardMarkup(keyboard=[[button_menu]], resize_keyboard=True, one_time_keyboard=True)

#docs_kb
button_form = InlineKeyboardButton(text="✏️Оформить документы", callback_data="form")
button_inspect = InlineKeyboardButton(text="📒Посмотреть свои документы", callback_data="inspect")
button_docs_back = InlineKeyboardButton(text="⬅️Назад", callback_data="docs_back")

docs_kb = InlineKeyboardMarkup(inline_keyboard=[[button_form], [button_inspect], [button_docs_back]])


button_inspect_back = InlineKeyboardButton(text="⬅️Назад", callback_data="inspect_back")
inspect_kb = InlineKeyboardMarkup(inline_keyboard=[[button_inspect_back]])

#front_kb