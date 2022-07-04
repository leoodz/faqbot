from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from FAQ.management.commands.keyboards.inline.keyboards import Keyboards
from FAQ.management.commands._loader import dp

# Creating an Instance of Keyboards
kb = Keyboards()


# The handler for the "Return to home" button should be above the handler for additional questions
@dp.callback_query_handler(text_contains="to_main")
async def on_main(call: CallbackQuery):
    await call.answer(cache_time=20)
    await call.message.answer(text=kb.setting.title_text,
                              reply_markup=kb.title_keyboard)
    await call.message.edit_reply_markup()


# Additional question handler
@dp.callback_query_handler(text_contains="sub")
async def applicate_mes(call: CallbackQuery):
    question = int(call.data.split(",")[1])
    answer = kb.questions[question][1]
    await call.answer(cache_time=20)
    await call.message.answer(answer,
                              reply_markup=kb.other_keyboards[question])
    await call.message.edit_reply_markup()


# start page
@dp.message_handler(Command("start"))
async def show_items(message: Message):
    await message.answer(text=kb.setting.title_text,
                         reply_markup=kb.title_keyboard)
