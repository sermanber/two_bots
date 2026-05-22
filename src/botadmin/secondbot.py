from local_settings import API_KEY_ADMIN
from aiogram.filters import CommandStart, Command
from aiogram import Bot, types
from aiogram import Dispatcher
import requests


admin_bot = Bot(token=API_KEY_ADMIN)
admin_dp = Dispatcher()


@admin_dp.message(CommandStart())
async def start(message: types.Message):
    await message.reply(f'! Я-бот-администратор мероприятий, сюда будут приходить запросы на проведение мероприятий')
    # response = requests.get(f'https://api.telegram.org/bot{API_KEY_ADMIN}/getUpdates')



@admin_dp.callback_query(lambda x: x.data.startswith(('approve', 'refuse')))
async def process_approve(callback_query: types.CallbackQuery):
    await admin_bot.answer_callback_query(callback_query.id)
    if callback_query.data[:-2] == 'approve':
        data = {'is_approved': 'Подтверждено'}
        bd_response = requests.post(f'http://127.0.0.1:8000/events/{callback_query.data[-2:]}/', data=data)
        if bd_response.status_code == 200:
            await callback_query.message.answer(text='Мероприятие одобрено')
        else:
            await callback_query.message.answer(text='Что-то пошло не так при одобрении')
    elif callback_query.data[:-2] == 'refuse':
        data = {'is_approved': 'Отказано'}
        bd_response = requests.post(f'http://127.0.0.1:8000/events/{callback_query.data[-2:]}/', data=data)
        if bd_response.status_code == 200:
            await callback_query.message.answer(text='Отказано')
        else:
            await callback_query.message.answer(text='Что-то пошло не так при отказе')
    else:
        await callback_query.message.answer(text='Что-то совсем пошло не так')



if __name__ == '__main__':
    admin_dp.run_polling(admin_bot)