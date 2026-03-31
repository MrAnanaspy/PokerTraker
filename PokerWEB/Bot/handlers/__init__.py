"""
Инициализатор пакета handlers.
Регистрирует все обработчики из разных файлов.
"""
import logging
from telegram.ext import Application

logger = logging.getLogger(__name__)


async def register_all_handlers(application: Application):
    """Регистрация всех обработчиков из разных модулей"""

    # Импортируем функции регистрации из каждого файла
    from .base import register_base_handlers
    from .registration import register_registration_handlers
    from .user_handlers import register_user_handlers

    logger.info("🔄 Начинаем регистрацию обработчиков...")

    # Регистрируем обработчики в правильном порядке
    # 1. Сначала регистрируем обработчики регистрации (самые важные)
    await register_registration_handlers(application)
    logger.info("✅ Зарегистрированы обработчики регистрации")

    # 2. Админские обработчики (если есть)


    # 3. Пользовательские обработчики (для зарегистрированных)
    try:
        await register_user_handlers(application)
        logger.info("✅ Зарегистрированы пользовательские обработчики")
    except ImportError:
        logger.warning("⚠️ Пользовательские обработчики не найдены, пропускаем...")

    # 4. Базовые обработчики (должны быть последними)
    await register_base_handlers(application)
    logger.info("✅ Зарегистрированы базовые обработчики")

    logger.info("🎉 Все обработчики успешно зарегистрированы!")

