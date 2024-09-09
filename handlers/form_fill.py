from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext

from keyboards.keyboards import menu_kb
from other.db_work import DBwork

db = DBwork("database_tck.db")

form_fill_router = Router()


class FillDocs(StatesGroup):
    name = State()
    surname = State()
    birth = State()
    fought = State()
    goden = State()
    judged = State()

#СТАРТ
@form_fill_router.callback_query(StateFilter(default_state), F.data == "form")
async def start_fill(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите ваше имя:", reply_markup=None)
    await state.set_state(FillDocs.name)



#ОТМЕНА
@form_fill_router.message(Command("cancel"), StateFilter(default_state))
async def start_fill(message: Message, state: FSMContext):
    await message.answer(text="""Вы ещё не начали заполнять анкету
    чтобы отменять её заполнение.

    Вернитесь в меню""", reply_markup=menu_kb)


@form_fill_router.message(Command("cancel"), ~StateFilter(default_state))
async def start_fill(message: Message, state: FSMContext):
    await message.answer(text="""Вы отменили заполнение анкеты.

Вернитесь в меню""", reply_markup=menu_kb)
    await state.clear()

#ИМЯ
@form_fill_router.message(StateFilter(FillDocs.name), F.text.isalpha())
async def fill_name(message: Message, state: FSMContext):
    await message.answer(text="Введите вашу фамилию:")
    await state.update_data(name=message.text)
    await state.set_state(FillDocs.surname)

@form_fill_router.message(StateFilter(FillDocs.name), F.text)
async def name_fail(message: Message, state: FSMContext):
    await message.answer(text="""Неверно введено имя.
Введите одним словом с большой буквы""")

#ФАМИЛИЯ
@form_fill_router.message(StateFilter(FillDocs.surname), F.text.istitle())
async def fill_name(message: Message, state: FSMContext):
    await message.answer(text="Введите ваш возраст")
    await state.update_data(surname=message.text)
    await state.set_state(FillDocs.birth)

@form_fill_router.message(StateFilter(FillDocs.surname), F.text)
async def name_fail(message: Message, state: FSMContext):
    await message.answer(text="""Неверно введена фамилия.
Введите с большой буквы""")

#ДАТА РОЖДЕНИЯ
@form_fill_router.message(StateFilter(FillDocs.birth), lambda x: x.text.isdigit() and 16 <= int(x.text) <= 120)
async def fill_name(message: Message, state: FSMContext):
    await message.answer(text="Воевали ли вы? да/нет")
    await state.update_data(birth=message.text)
    await state.set_state(FillDocs.fought)

@form_fill_router.message(StateFilter(FillDocs.birth), F.text)
async def name_fail(message: Message, state: FSMContext):
    await message.answer(text="""Неверно введён возраст. Введите число""")

#ВОЕВАЛ
@form_fill_router.message(StateFilter(FillDocs.fought), or_f(F.text.casefold() == "нет", F.text.casefold() == "да"))
async def fill_name(message: Message, state: FSMContext):
    await message.answer(text="Вы годен? да/нет")
    await state.update_data(fought=message.text.title())
    await state.set_state(FillDocs.goden)

@form_fill_router.message(StateFilter(FillDocs.fought), F.text)
async def name_fail(message: Message, state: FSMContext):
    await message.answer(text="Неверно введены данные. Введите да или нет")

#ГОДЕН
@form_fill_router.message(StateFilter(FillDocs.goden), or_f(F.text.casefold() == "нет", F.text.casefold() == "да"))
async def fill_name(message: Message, state: FSMContext):
    await message.answer(text="У вас есть судимость? да/нет:")
    await state.update_data(goden=message.text.title())
    await state.set_state(FillDocs.judged)

@form_fill_router.message(StateFilter(FillDocs.goden), F.text)
async def name_fail(message: Message, state: FSMContext):
    await message.answer(text="Неверно введены данные. Введите да или нет")

#СУДИМОСТЬ
@form_fill_router.message(StateFilter(FillDocs.judged), or_f(F.text.casefold() == "нет", F.text.casefold() == "да"))
async def fill_name(message: Message, state: FSMContext):
    await state.update_data(judged=message.text.title())
    data = await state.get_data()
    await message.answer(text=f"""Ваши документы заполнены.
Имя: {data["name"]}
Фамилия: {data["surname"]}
Возраст: {data["birth"]}
Служил: {data["fought"]}
Годен: {data["goden"]}
Судимость: {data["judged"]}""", reply_markup=menu_kb)
    db.reg_docs(message.from_user.id, data["name"], data["surname"], data["birth"], data["fought"], data["goden"], data["judged"])
    await state.clear()


@form_fill_router.message(StateFilter(FillDocs.judged), F.text)
async def name_fail(message: Message, state: FSMContext):
    await message.answer(text="Неверно введены данные Введите да или нет")
