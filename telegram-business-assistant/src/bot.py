"""Application entry point."""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from src.application.enquiries import EnquiryService
from src.application.notifications import (
    NotificationOutboxDispatcher,
    run_outbox_worker,
)
from src.config import Settings
from src.database import Database
from src.handlers import router
from src.infrastructure.telegram_notifications import TelegramLeadNotificationSender


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    settings = Settings.from_env()
    database = Database(settings.database_path)
    await database.initialize()
    enquiry_service = EnquiryService(database)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher(storage=MemoryStorage())
    notification_dispatcher = NotificationOutboxDispatcher(
        database,
        TelegramLeadNotificationSender(bot),
    )
    stop_worker = asyncio.Event()
    worker_task = asyncio.create_task(
        run_outbox_worker(notification_dispatcher, stop_worker)
    )
    dispatcher["db"] = database
    dispatcher["enquiry_service"] = enquiry_service
    dispatcher["settings"] = settings
    dispatcher.include_router(router)

    try:
        await dispatcher.start_polling(
            bot,
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
    finally:
        stop_worker.set()
        await worker_task
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
