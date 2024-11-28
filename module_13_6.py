from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kbi = InlineKeyboardMarkup()
buttoni = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='Калории')
buttoni1 = InlineKeyboardButton(text='Формулы рассчёта', callback_data='Формулы')

button = KeyboardButton(text='Информация!')
button2 = KeyboardButton(text='Расчитать')
kb.add(button, button2)
kbi.add(buttoni, buttoni1)


@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kbi)


@dp.callback_query_handler(text='Формулы')
async def get_formulas(call):
    await call.message.answer('10 * вес(кг) + 6.25 * рост (см) – 4.92 * возраст – 161')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler(text='Информация!')
async def button1(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='Калории')
async def set_age(call):
    await call.message.answer('Введите свой возраст(г):', reply_markup=kb)
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост(см):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес(кг):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    await message.answer(f'Ваша норма калорий: {10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] - 161}')
    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start или нажмите кнопку "Информация!" чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
