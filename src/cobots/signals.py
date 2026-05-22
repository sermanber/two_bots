from django.forms import model_to_dict
from botadmin.local_settings import API_KEY_ADMIN
from bot.local_settings import API_KEY
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cobots
from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



@receiver(post_save, sender=Cobots)
async def change(sender, instance, **kwargs):
    admin_bot = Bot(API_KEY_ADMIN)
    updated_data = model_to_dict(instance)
    # Чтобы сообщение приходило не на все апдэйты, а только на непросмотренные is_approved == None
    if updated_data['is_approved'] is None:
        # ID чата с ботом администратором
        chat_id = 245144717
        message_text = (f"Мероприятие: {updated_data['event']}\n"
                        f"Место: {updated_data['place']}\n"
                        f"Ведущий мероприятия: {updated_data['name']}")


        rows = [
            InlineKeyboardButton(text='Подтвердить', callback_data=f'approve{updated_data["id"]}'),
            InlineKeyboardButton(text='Отказать', callback_data=f'refuse{updated_data["id"]}')
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[rows])

        await admin_bot.send_message(chat_id=chat_id, text=message_text, reply_markup=keyboard)

    if updated_data['is_approved']:
        bot = Bot(API_KEY)
        updated_data = model_to_dict(instance)

        chat_id = updated_data['user_chat_id']
        message_text = (updated_data['is_approved'])


        await bot.send_message(chat_id=chat_id, text=message_text)