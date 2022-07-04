import logging
import sys
from aiogram import Bot, Dispatcher
from FAQ.management.commands.base_connect import BotQueries


# Настройки логирования

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )

BOT_TOKEN = sys.argv[2]


# Инициализация базы данных
db = BotQueries(BOT_TOKEN)

# Инициализация бота и диспатчера
try:
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot)
    print(f"Bot enabled ID = {db.bot_id}")
    db.change_bot_status(status='on',token=str(BOT_TOKEN))
except BaseException as err:
    print(f"An error has occurred {err} when starting the bot ID = {db.bot_id}")
    db.change_bot_status(status='off',token=str(BOT_TOKEN))