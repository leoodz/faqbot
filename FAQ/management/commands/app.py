import asyncio
from aiogram import executor
from django.core.management import BaseCommand
from FAQ.management.commands.handlers import dp
from FAQ.management.commands.handlers.users.questions import kb


async def on_startup(x):
    """Running Asynchronous Update Checking Functions"""
    asyncio.create_task(kb.bot_updater())

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)


class Command(BaseCommand):
    """Class to run script via manage.py"""
    help: str = 'Enable bot'

    def handle(self, *args, **options):
        executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)

    def add_arguments(self, parser):
        parser.add_argument('args', nargs='*')
