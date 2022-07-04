from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Questions(models.Model):
    """Таблица для хранения вопросов"""
    question = models.CharField(max_length=30, verbose_name="Вопрос")
    answer = models.TextField(default="No text", verbose_name="Ответ на вопрос")
    id = models.BigAutoField(primary_key=True)
    bot = models.ForeignKey("SettingsBot", related_name="Бот", on_delete=models.CASCADE,
                            verbose_name="Бот")
    general = models.BooleanField(default=False, verbose_name="Отображать на стартовой странице")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Изменен")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ('-id',)

    def get_absolute_url(self):
        return reverse('FAQ:edit_questions', kwargs={'question_id': self.id,
                                                     'bot_id': self.bot.id})

    def __str__(self):
        return self.question

    def data(self):
        return [self.question, self.answer, self.id, self.general]


class RelationQuestion(models.Model):
    """Таблица для хранения связей вопросов"""
    base = models.ForeignKey("Questions", related_name='Основной_вопрос', on_delete=models.CASCADE, verbose_name="Основной вопрос")
    sub = models.ForeignKey("Questions", related_name='Дополнительный_вопрос', on_delete=models.CASCADE, verbose_name="Дополнительный вопрос")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Изменен")

    class Meta:
        verbose_name = "Таблица связей вопросов"
        verbose_name_plural = "Таблица связей вопросов"
        unique_together = (("base", "sub"),)


class SettingsBot(models.Model):
    """Таблица настроек бота"""
    STATUS_CHOICES = (
        ('включен', 'Включен'),
        ('выключен', 'Выключен'),
        ('неверный токен', 'Неверный токен'),
    )
    id = models.BigAutoField(primary_key=True)
    bot_name = models.CharField(max_length=50, verbose_name="Название")
    status = models.CharField(max_length=20, verbose_name="Статус", choices=STATUS_CHOICES, default='выключен')
    user = models.ForeignKey(User, related_name='settings_bots', on_delete=models.CASCADE)
    title_question = models.TextField(default="Добрый день!\nКакой у вас воопрос?", verbose_name="Титульное сообщение")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Изменен")
    token = models.CharField(default="", max_length=50, unique=True, verbose_name="Токен")
    title_button_row = models.IntegerField(default=2, verbose_name="Количество столбцов кнопок титульного вопроса", validators=[
        MaxValueValidator(8),
        MinValueValidator(1)
    ])
    other_button_row = models.IntegerField(default=2, verbose_name="Количество столбцов кнопок дополнительных вопросов", validators=[
        MaxValueValidator(8),
        MinValueValidator(1)
    ])
    interval_refresh_base = models.IntegerField(default=20, verbose_name="Интервал синхронизации вопросов в сек", validators=[
        MinValueValidator(20)
    ])

    class Meta:
        verbose_name = "Настройки бота"
        verbose_name_plural = "Настройки бота"
        ordering = ('status', '-id')

    def __str__(self):
        return str(self.bot_name)

    def get_absolute_url(self):
        return reverse('FAQ:settings_bot_detail', kwargs={'bot_id': str(self.id)})

    def data(self):
        return [self.user, self.token, self.id, self.updated]