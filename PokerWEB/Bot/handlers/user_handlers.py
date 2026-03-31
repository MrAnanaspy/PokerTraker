"""
Обработчики команд для зарегистрированных пользователей
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler
)
from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

# Импорт моделей
from User.models import Users


# Декоратор для проверки регистрации
def registered_required(func):
    """Декоратор для команд, требующих регистрации"""
    from functools import wraps

    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_tg = update.effective_user
        print(1)

        # Проверяем регистрацию
        from .registration import check_user_registration
        is_registered = await check_user_registration(user_tg.id)

        if not is_registered:
            print("DEBUG: Пользователь не зарегистрирован, отправляем сообщение")

            # Используем HTML разметку вместо Markdown (она более надежная)
            text = (
                "🔐 <b>Эта команда только для зарегистрированных пользователей</b>\n\n"
                "Для регистрации используйте:\n"
                "<code>/reg ваш_никнейм</code>\n\n"
                "Инструкция: /register_help"
            )

            try:
                # Отправляем сообщение через бота с HTML разметкой
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=text,
                    parse_mode='HTML'  # Используем HTML вместо Markdown
                )
                print("DEBUG: Сообщение отправлено успешно")
            except Exception as e:
                print(f"DEBUG: Ошибка отправки: {e}")
                # Пробуем без разметки
                try:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=(
                            "🔐 Эта команда только для зарегистрированных пользователей\n\n"
                            "Для регистрации используйте:\n"
                            "/reg ваш_никнейм\n\n"
                            "Инструкция: /register_help"
                        )
                    )
                except Exception as e2:
                    print(f"DEBUG: Вторая ошибка отправки: {e2}")

            return

        return await func(update, context, *args, **kwargs)

    return wrapper


async def register_user_handlers(application):
    """Регистрация пользовательских обработчиков"""

    # Команда /profile - только для зарегистрированных
    application.add_handler(CommandHandler("profile", profile_command))

    # Команда /games
    application.add_handler(CommandHandler("games", games_command))

    # Команда /settings
    application.add_handler(CommandHandler("settings", settings_command))

    # Команда /balance
    application.add_handler(CommandHandler("balance", balance_command))

    # Команда /history
    application.add_handler(CommandHandler("history", history_command))

    # Обработчик inline кнопок
    application.add_handler(CallbackQueryHandler(button_callback, pattern="^user_"))


# ========== КОМАНДЫ ДЛЯ ЗАРЕГИСТРИРОВАННЫХ ==========

@registered_required
async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /profile - показывает профиль пользователя"""
    user_tg = update.effective_user

    @sync_to_async
    def get_user_profile():
        try:
            return Users.objects.get(telegram_id=user_tg.id)
        except Users.DoesNotExist:
            return None

    user = await get_user_profile()

    if not user:
        await update.message.reply_text("❌ Ошибка загрузки профиля")
        return

    # Создаем клавиатуру
    keyboard = [
        [
            InlineKeyboardButton("Посмотреть данные еще раз", callback_data="get_user_profile"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    profile_text = f"""
    👤 *Ваш профиль:*

    *Основное:*
    • Никнейм: {user.username}

    *Telegram:*
    • ID: {user_tg.id}

    *Статус:*
    • Рейтинг: {user.score}
    """

    await update.message.reply_text(
        profile_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


@registered_required
async def games_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /profile - показывает профиль пользователя"""
    user_tg = update.effective_user

    @sync_to_async
    def get_user_profile():
        try:
            return Users.objects.get(telegram_id=user_tg.id)
        except Users.DoesNotExist:
            return None

    @sync_to_async
    def get_games():
        try:
            return Users.objects.get(telegram_id=user_tg.id)
        except Users.DoesNotExist:
            return None

    user = await get_user_profile()
    games = await get_games()

    if not user:
        await update.message.reply_text("❌ Ошибка загрузки профиля")
        return

    # Создаем клавиатуру
    keyboard = [
        [
            InlineKeyboardButton("✏️ Изменить данные", callback_data="user_edit_profile"),
            InlineKeyboardButton("🔐 Безопасность", callback_data="user_security")
        ],
        [
            InlineKeyboardButton("💳 Баланс", callback_data="user_balance"),
            InlineKeyboardButton("📊 Статистика", callback_data="user_stats")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    profile_text = f"""
    👤 *оследние игры:*

    *Не законченые:*
    • Никнейм: {user.nickname}

    *Telegram:*
    • ID: {user_tg.id}

    *Статус:*
    • Рейтинг: {user.score}
    """

    await update.message.reply_text(
        profile_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )


@registered_required
async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Настройки пользователя"""
    await update.message.reply_text(
        "⚙️ *Настройки*\n\n"
        "Выберите раздел для настройки:\n\n"
        "• /notifications - Управление уведомлениями\n"
        "• /privacy - Настройки приватности\n"
        "• /language - Выбор языка\n\n"
        "Или используйте кнопки в меню профиля.",
        parse_mode='Markdown'
    )


@registered_required
async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает баланс пользователя"""
    user_tg = update.effective_user

    @sync_to_async
    def get_user_balance():
        try:
            user = Users.objects.get(telegram_id=user_tg.id)
            # Предполагаем, что у модели Users есть поле balance
            return getattr(user, 'balance', 0)
        except Users.DoesNotExist:
            return 0

    balance = await get_user_balance()

    await update.message.reply_text(
        f"💰 *Ваш баланс:* {balance} ₽\n\n"
        f"💳 Для пополнения баланса обратитесь в поддержку.\n"
        f"📊 История операций: /history",
        parse_mode='Markdown'
    )


@registered_required
async def history_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """История операций пользователя"""
    await update.message.reply_text(
        "📜 *История операций*\n\n"
        "Здесь будет отображаться история ваших операций.\n\n"
        "Функция находится в разработке.\n"
        "Скоро здесь появится:\n"
        "• История платежей\n"
        "• История действий\n"
        "• Статистика использования\n\n"
        "Следите за обновлениями!",
        parse_mode='Markdown'
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на inline кнопки"""
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "user_edit_profile":
        await query.edit_message_text(
            "✏️ *Изменение профиля*\n\n"
            "Для изменения данных профиля обратитесь в поддержку:\n"
            "/support\n\n"
            "Или измените данные в личном кабинете на сайте.",
            parse_mode='Markdown'
        )
    elif data == "user_balance":
        await balance_command(update, context)
    elif data == "user_stats":
        await query.edit_message_text(
            "📊 *Статистика*\n\n"
            "Статистика использования сервиса.\n"
            "Функция в разработке.\n\n"
            "Скоро здесь появится:\n"
            "• Активность по дням\n"
            "• Количество операций\n"
            "• Графики использования",
            parse_mode='Markdown'
        )