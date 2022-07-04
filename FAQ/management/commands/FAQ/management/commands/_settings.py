from FAQ.management.commands._loader import db


class Settings:
    """Настройки телеграм бота"""

    def __init__(self):

        self.settings_data = db.get_settings_bot()
        self.title_text = self.settings_data[0]
        self.interval_refresh_base = self.settings_data[1]
        self.title_button_row = self.settings_data[2]
        self.other_button_row = self.settings_data[3]