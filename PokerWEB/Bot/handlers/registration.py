import logging
from functools import wraps

from django.contrib.auth import authenticate
from telegram import Update
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
import os
import django
import sys
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Добавьте это в начало файла
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Теперь импортируем модели
from User.models import Users

logger = logging.getLogger(__name__)


async def register_registration_handlers(application):
    """Регистрация обработчиков регистрации"""

    # Команда регистрации
    application.add_handler(CommandHandler("reg", registration_command))
# Функция проверки регистрации
async def check_user_registration(telegram_id: int) -> bool:
    """Проверяет, зарегистрирован ли пользователь"""
    try:
        # Используем sync_to_async правильно
        return await sync_to_async(lambda: Users.objects.filter(telegram_id=telegram_id).exists())()
    except Exception as e:
        logger.error(f"Error checking registration: {e}")
        return False


async def registration_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /reg"""
    user_tg = update.effective_user

    # Проверяем, не зарегистрирован ли уже пользователь
    is_registered = await check_user_registration(user_tg.id)

    if is_registered:
        await update.message.reply_text(
            "✅ Вы уже зарегистрированы!\n\n"
            "Используйте /profile для просмотра профиля\n"
            "Или /help для списка всех команд"
        )
        return

    # Проверяем аргументы команды
    if not context.args:
        await update.message.reply_text(
            "📝 *Использование команды:*\n\n"
            "`/reg ваш_никнейм`\n\n"
            "*Пример:*\n"
            "`/reg ivan123`\n\n"
            "Где взять никнейм? Смотрите в личном кабинете на сайте.",
            parse_mode='Markdown'
        )
        return

    nickname = context.args[0]
    password = context.args[1]

    try:
        # Ищем пользователя в базе
        @sync_to_async
        def find_and_update_user():
            try:
                user = authenticate(username=nickname, password=password)

                # Проверяем, не привязан ли уже Telegram
                if user.telegram_id:
                    return {
                        'success': False,
                        'error': 'Этот аккаунт уже привязан к другому Telegram'
                    }

                # Обновляем данные
                user.telegram_id = user_tg.id
                user.telegram_username = user_tg.username
                user.telegram_first_name = user_tg.first_name
                user.save()

                return {
                    'success': True,
                    'user': user
                }

            except Users.DoesNotExist:
                return {
                    'success': False,
                    'error': 'Неправильный никнейм или пароль'
                }

        result = await find_and_update_user()

        if result['success']:
            await update.message.reply_text(
                f"🎉 *Регистрация успешна!*\n\n"
                f"✅ Аккаунт *{result['user'].username}* привязан к Telegram.\n\n"
                f"📋 *Ваши данные:*\n"
                f"• Никнейм: {result['user'].username}\n"
                f"• Telegram ID: {user_tg.id}\n"
                f"• Имя: {user_tg.first_name}\n\n"
                f"Теперь вам доступны все команды бота!\n"
                f"Используйте /profile для просмотра профиля.",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(f"❌ {result['error']}")

    except Exception as e:
        logger.error(f"Registration error: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при регистрации.\n"
            "Пожалуйста, попробуйте позже или обратитесь в поддержку."
        )