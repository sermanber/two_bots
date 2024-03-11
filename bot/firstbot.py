from local_settings import API_KEY
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import requests


bot = Bot(token=API_KEY)
dp = Dispatcher()

class FSMFillForm(StatesGroup):
    fill_event = State()
    fill_place = State()
    fill_name = State()


user_dict = {}

@dp.message(CommandStart(), StateFilter(default_state))
async def command_start(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=f'Привет, {message.from_user.full_name}\n'
                              f'! Я-бот мероприятий. Чтобы перейти к заполнению анкеты отправьте команду /fillform')


@dp.message(Command(commands='fillform'), StateFilter(default_state))
async def process_fill_form(message: Message, state: FSMContext):
    # Запрашиваем название мероприятия
    await message.answer(text='Пожалуйста, введите название вашего мероприятия')
    await state.set_state(FSMFillForm.fill_event)


@dp.message(StateFilter(FSMFillForm.fill_event))
async def get_event(message: Message, state: FSMContext):
    # Получаем название мероприятия
    await state.update_data(event=message.text)
    # Запрашиваем ссылку мероприятия
    await message.answer(text='Спасибо!\n\nА теперь введите ссылку мероприятия')
    await state.set_state(FSMFillForm.fill_place)


@dp.message(StateFilter(FSMFillForm.fill_place))
async def get_place(message: Message, state: FSMContext):
    # Получаем ссылку мероприятия
    await state.update_data(place=message.text)
    # Запрашиваем имя ведущего
    await message.answer(text='Спасибо!\n\nА теперь введите имя ведущего мероприятия')
    await state.set_state(FSMFillForm.fill_name)


@dp.message(StateFilter(FSMFillForm.fill_name))
async def get_name(message: Message, state: FSMContext):
    # Получаем имя ведущего
    await state.update_data(name=message.text)
    # Добавляем в словарь анкету пользователя
    user_dict[message.from_user.id] = await state.get_data()
    # Сбрасываем машину состояния
    await state.clear()
    # Добавляем данные в базу данных
    data = user_dict[message.from_user.id]
    data.update({'user_chat_id': message.from_user.id})
    bd_response = requests.post('http://127.0.0.1:8000/events/', data=data)
    print(user_dict[message.from_user.id], bd_response.status_code)
    if bd_response.status_code == 201:
        await message.answer(text='Готово! Ожидайте ответа оператора, а пока можете посмотреть анкету /showdata')
    else:
        await message.answer(text='Что-то пошло не так, ппопробуйте заполнить анкету ещё раз /fillform')


@dp.message(Command(commands='showdata'), StateFilter(default_state))
async def showdata(message: Message):
    # Отправляем пользователю анкету, если она есть в словаре
    if message.from_user.id in user_dict:
        await message.answer(text=(f'Мероприятие: {user_dict[message.from_user.id]["event"]}\n'
                                   f'Место: {user_dict[message.from_user.id]["place"]}\n'
                                   f'Ведущий: {user_dict[message.from_user.id]["name"]}\n'))
    else:
        # Если анкеты нет, предлагаем заполнить
        await message.answer(text='Вы еще не заполняли анкету. Чтобы приступить - '
                                  'отправьте команду /fillform')

if __name__ == '__main__':
    dp.run_polling(bot)


