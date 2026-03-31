import os
import sys
import django
import asyncio
import logging
from django.core.management.base import BaseCommand
from django.conf import settings

# Настройка Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Импорт после django.setup()
from telegram.ext import Application
from Bot.handlers import register_all_handlers

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Запуск Telegram бота с разделенными обработчиками'

    def handle(self, *args, **options):
        if not settings.TELEGRAM_BOT_TOKEN:
            self.stderr.write("❌ TELEGRAM_BOT_TOKEN не установлен!")
            return

        self.stdout.write("🚀 Запуск бота с разделенными обработчиками...")

        try:
            asyncio.run(self.main())
        except KeyboardInterrupt:
            self.stdout.write("\n⏹ Бот остановлен")
        except Exception as e:
            logger.error(f"Ошибка запуска: {e}")
            self.stderr.write(f"❌ Ошибка: {e}")

    async def main(self):
        """Основная асинхронная функция"""
        # Создаем приложение бота
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # Регистрируем ВСЕ обработчики из разных файлов
        await register_all_handlers(application)

        # Запускаем бота
        self.stdout.write("✅ Бот запущен")
        self.stdout.write("📡 Ожидание сообщений...")

        await application.initialize()
        await application.start()
        await application.updater.start_polling()

        # Бесконечное ожидание
        await asyncio.Event().wait()