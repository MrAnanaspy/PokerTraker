from django.db.models.signals import post_save
from django.dispatch import receiver
import threading
import asyncio
from asgiref.sync import sync_to_async
from telegram import Bot
from User.models import Users
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .models import Tournament
from PokerWEB.settings import TELEGRAM_BOT_TOKEN


@receiver(post_save, sender=Tournament)
def tournament_created(sender, instance, created, **kwargs):
    if created:
        print(1)
        threading.Thread(
            target=send_notifications_sync,
            args=(instance,),
            daemon=True
        ).start()


def send_notifications_sync(tournament):
    asyncio.run(send_notifications_async(tournament))


async def send_notifications_async(tournament):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    users = await sync_to_async(list)(
        Users.objects.exclude(telegram_id=None)
    )

    for user in users:
        try:
            keyboard = [
                [InlineKeyboardButton("✏️ Записаться", callback_data=f"join_{tournament.id}")]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            await bot.send_message(
                chat_id=user.telegram_id,
                text=f"""🎮 <b>Новая игра</b>

🆔 <b>Номер:</b> {tournament.id}
📅 <b>Сезон:</b> {tournament.season.name}
⏰ <b>Дата:</b> {tournament.date}

💰 <b>Стартовый стек:</b> {tournament.stack}
🎟 <b>Стоимость входа:</b> {tournament.cost}
⏳ <b>Время игры:</b> {tournament.time}
""",
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        except Exception as e:
            print(e)