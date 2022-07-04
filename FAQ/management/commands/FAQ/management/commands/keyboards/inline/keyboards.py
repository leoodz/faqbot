import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from FAQ.management.commands._loader import db, BOT_TOKEN
from FAQ.management.commands._settings import Settings


class Keyboards:
    """Класс для управления клавиатурами бота"""

    def __init__(self):
        # Инициализация настроек
        self.setting = Settings()
        # Получение вопросов и связей из базы данных
        self.questions = db.get_all_questions()
        self.relations = db.get_questions_relations()
        # Получение даты последнего изменения базы для контроля обновлений
        self.last_update = db.get_last_update()
        # Создание словарей клавиатур и ответов
        self.add_button_to_all_keyboards("Вернуться на главную", "to_main")
        # Инициализация клавиатур
        self.title_keyboard = InlineKeyboardMarkup(row_width=self.setting.title_button_row)
        self.create_title_keyboard_button()
        self.other_keyboards = {question_id: InlineKeyboardMarkup(row_width=self.setting.other_button_row)
                                for question_id in self.questions.keys()}
        self.create_other_keyboard_button()


    def create_title_keyboard_button(self):
        """Создание кнопок для стартовой клавиатуры"""
        for question, data in self.questions.items():
            if data[2]:
                button = InlineKeyboardButton(text=data[0], callback_data=f"sub,{question}")
                self.title_keyboard.insert(button)

    def create_other_keyboard_button(self):
        """Создание кнопок для дополнительных клавиатур"""
        for question in self.questions:
            for relation in self.relations:
                if relation[0] == question:
                    button = InlineKeyboardButton(text=self.questions[relation[1]][0], callback_data=f"sub,{relation[1]}")
                    self.other_keyboards[question].insert(button)

    def add_button_to_all_keyboards(self, text, callback_data):
        """Функция добавления кнопки во все клавиатуры, кроме стартовой"""
        for question in self.questions:
            try:
                if int(question):
                    self.relations.append((question, callback_data))
            except TypeError:
                print(question + " - не число")
        self.questions.update({callback_data: (text, 0, 0)})

    async def bot_updater(self):
        """Обновление кнопок бота при изменении базы"""
        while True:
            db.__init__(BOT_TOKEN)
            if self.last_update == db.get_last_update():
                print(f'Бот {db.bot_id} обновления отсутствуют')
            else:
                self.__init__()
                print(f'Данные обновлены {self.last_update.strftime("%d %B %Y %I:%M%p")} бот {db.bot_id}')
            await asyncio.sleep(self.setting.interval_refresh_base)
