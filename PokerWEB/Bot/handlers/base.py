"""
Базовые команды бота: /start, /help, /info
"""
import logging
from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

logger = logging.getLogger(__name__)


async def register_base_handlers(application):
    """Регистрация базовых обработчиков"""

    # Команда /start
    application.add_handler(CommandHandler("start", start_command))

    # Команда /help
    application.add_handler(CommandHandler("help", help_command))

    # Команда /info
    application.add_handler(CommandHandler("info", info_command))


    # Обработчик ошибок
    application.add_error_handler(error_handler)


# ========== ОБРАБОТЧИКИ КОМАНД ==========

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user

    welcome_text = f"""
    👋 Привет, {user.first_name}!

    Для начала тебе нужно зарегистрироваться!

    📋 /reg nickname
    """

    await update.message.reply_text(welcome_text)
    logger.info(f"Пользователь {user.id} вызвал /start")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
    🆘 *Помощь по командам:*

    *👤 Пользовательские команды:*
    /profile - Ваш профиль
    /settings - Настройки
    /feedback - Оставить отзыв

    *⚙️ Админские команды:*
    /admin - Админ-панель
    /stats - Статистика
    /broadcast - Рассылка

    *📌 Общие команды:*
    /start - Начать работу
    /help - Эта справка
    /cancel - Отмена действия

    Для связи с поддержкой: @support_username
    """

    await update.message.reply_text(help_text, parse_mode='Markdown')
    logger.info(f"Пользователь {update.effective_user.id} вызвал /help")


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /info"""
    info_text = """
    🤖 *Информация о боте:*

    *Версия:* 2.0.0
    *Разработчик:* Ваша компания
    *Платформа:* Django + python-telegram-bot
    *Архитектура:* Модульные обработчики

    *Особенности:*
    • Разделенные файлы обработчиков
    • Поддержка админ-панели
    • Работа с базой данных
    • Inline кнопки
    • Логирование действий

    Исходный код: [GitHub](https://github.com/your-repo)
    """

    await update.message.reply_text(info_text, parse_mode='Markdown')


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик всех текстовых сообщений"""
    text = update.message.text
    user = update.effective_user
    print(user.id)
    logger.info(f"Пользователь {user.id} отправил: {text}")

    # Простой эхо-ответ
    response = f"📝 {user.username} написали: {text}\n\nИспользуйте /reg [nikname] [password] для регистрации"
    await context.bot.send_message(chat_id='1698495462', text=response)
    await update.message.reply_text(response)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Глобальный обработчик ошибок"""
    logger.error(f"Ошибка в обновлении {update}: {context.error}", exc_info=True)

    # Отправляем сообщение об ошибке пользователю
    if update and update.effective_chat:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="😕 Произошла ошибка. Пожалуйста, попробуйте позже."
            )
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение об ошибке: {e}")