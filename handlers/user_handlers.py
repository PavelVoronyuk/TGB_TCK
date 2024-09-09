from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, or_f

from lexicon.lexicon import LEXICON_RU
from keyboards.keyboards import start_kb, docs_kb, inspect_kb, menu_kb
from other.db_work import DBwork

user_router = Router()

db = DBwork("database_tck.db")

@user_router.message(or_f(CommandStart(), F.text == "В меню"))
async def start(message: Message):
    if message.chat.type == "private":
        if not db.check_user(message.from_user.id):
            db.add_user(message.from_user.id)
    await message.answer(LEXICON_RU["/start"], reply_markup=start_kb)


#Документы
@user_router.callback_query(F.data == "docs_start")
async def docs_menu(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU["docs_menu"], reply_markup=docs_kb)

@user_router.callback_query(F.data == "docs_back")
async def docs_back(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU["/start"], reply_markup=start_kb)

@user_router.callback_query(F.data == "inspect")
async def inspect(callback: CallbackQuery):
    if db.check_docs(callback.from_user.id):
        await callback.message.edit_text(text=db.get_docs(callback.from_user.id), reply_markup=inspect_kb)
    else:
        await callback.message.answer(text="Вы ещё не заполнили документы!", reply_markup=inspect_kb)

@user_router.callback_query(F.data == "inspect_back")
async def inspect_back(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU["/start"], reply_markup=start_kb)

#На фронт
