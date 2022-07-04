import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from FAQ.management.commands._loader import db, BOT_TOKEN
from FAQ.management.commands._settings import Settings


class Keyboards:
    """Class for managing bot keyboards"""

    def __init__(self):
        # Initializing settings
        self.setting = Settings()
        # Retrieving questions and relationships from the database
        self.questions = db.get_all_questions()
        self.relations = db.get_questions_relations()
        # Getting the date of the last change of the database for update control
        self.last_update = db.get_last_update()
        # Создание словарей клавиатур и ответов
        self.add_button_to_all_keyboards("Go back to the main page", "to_main")
        # Creating keyboard and response dictionaries
        self.title_keyboard = InlineKeyboardMarkup(row_width=self.setting.title_button_row)
        self.create_title_keyboard_button()
        self.other_keyboards = {question_id: InlineKeyboardMarkup(row_width=self.setting.other_button_row)
                                for question_id in self.questions.keys()}
        self.create_other_keyboard_button()


    def create_title_keyboard_button(self):
        """Creating buttons for the start keyboard"""
        for question, data in self.questions.items():
            if data[2]:
                button = InlineKeyboardButton(text=data[0], callback_data=f"sub,{question}")
                self.title_keyboard.insert(button)

    def create_other_keyboard_button(self):
        """Creating buttons for additional keyboards"""
        for question in self.questions:
            for relation in self.relations:
                if relation[0] == question:
                    button = InlineKeyboardButton(text=self.questions[relation[1]][0], callback_data=f"sub,{relation[1]}")
                    self.other_keyboards[question].insert(button)

    def add_button_to_all_keyboards(self, text, callback_data):
        """The function of adding a button to all keyboards, except for the start one"""
        for question in self.questions:
            try:
                if int(question):
                    self.relations.append((question, callback_data))
            except TypeError:
                print(question + " - not a number")
        self.questions.update({callback_data: (text, 0, 0)})

    async def bot_updater(self):
        """Update bot buttons on base change"""
        while True:
            db.__init__(BOT_TOKEN)
            if self.last_update == db.get_last_update():
                print(f'Bot {db.bot_id} no updates')
            else:
                self.__init__()
                print(f'Data updated {self.last_update.strftime("%d %B %Y %I:%M%p")} bot {db.bot_id}')
            await asyncio.sleep(self.setting.interval_refresh_base)
