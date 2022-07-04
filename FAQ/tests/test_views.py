import pprint

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from FAQ.urls import *


class ViewTestCase(TestCase):
    def setUp(self):
        # Пользователи
        self.user1 = User.objects.create(username="test_user1")
        self.user2 = User.objects.create(username="test_user2")
        # Боты
        self.bot1 = SettingsBot.objects.create(bot_name="bot1",
                                               user=self.user1,
                                               token="qweqweqweqweqweqweqwe1")
        self.bot2 = SettingsBot.objects.create(bot_name="bot2",
                                               user=self.user1,
                                               token="qweqweqweqweqweqweqwe2")
        self.bot3 = SettingsBot.objects.create(bot_name="bot3",
                                               user=self.user1,
                                               token="qweqweqweqweqweqweqwe3")
        self.bot4 = SettingsBot.objects.create(bot_name="bot4",
                                               user=self.user2,
                                               token="qweqweqweqweqweqweqwe4")
        self.bot5 = SettingsBot.objects.create(bot_name="bot5",
                                               user=self.user2,
                                               token="qweqweqweqweqweqweqwe5")
        # Вопросы
        self.question1 = Questions.objects.create(question="question1",
                                                  answer="answer1",
                                                  bot=self.bot2)
        self.question2 = Questions.objects.create(question="question2",
                                                  answer="answer2",
                                                  bot=self.bot2)
        self.question3 = Questions.objects.create(question="question3",
                                                  answer="answer3",
                                                  bot=self.bot2)
        self.question4 = Questions.objects.create(question="question4",
                                                  answer="answer4",
                                                  bot=self.bot2)
        self.question5 = Questions.objects.create(question="question5",
                                                  answer="answer5",
                                                  bot=self.bot1)
        self.question6 = Questions.objects.create(question="question6",
                                                  answer="answer6",
                                                  bot=self.bot1)
        self.question7 = Questions.objects.create(question="question7",
                                                  answer="answer7",
                                                  bot=self.bot1)
        self.question8 = Questions.objects.create(question="question8",
                                                  answer="answer8",
                                                  bot=self.bot1)
        # Связи вопросов
        self.relationquestion1 = RelationQuestion.objects.create(base=self.question5,
                                                                 sub=self.question6)
        self.relationquestion2 = RelationQuestion.objects.create(base=self.question5,
                                                                 sub=self.question7)

    def test_bot_list(self):
        self.client.force_login(self.user1)
        url = reverse("FAQ:bot_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['bots']),
                         '<QuerySet [<SettingsBot: bot3>, <SettingsBot: bot2>, <SettingsBot: bot1>]>')

    def test_create_bot(self):
        self.assertEqual(SettingsBot.objects.all().count(), 5)
        self.client.force_login(self.user1)
        url = reverse("FAQ:create_bot")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'bot_name': 'bot6',
                'status': 'выключен',
                'title_question': 'ok',
                'title_button_row': 4,
                'other_button_row': 4,
                'interval_refresh_base': 33,
                'token': 'qweqweqweqweqweqweqwe6'}
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(SettingsBot.objects.all().count(), 6)
        bot = get_object_or_404(SettingsBot, token=data['token'], user=self.user1)
        self.assertEqual(bot.bot_name, 'bot6')

    def test_edit_settings_bot(self):
        self.client.force_login(self.user1)
        bot = get_object_or_404(SettingsBot, token='qweqweqweqweqweqweqwe2', user=self.user1)
        url = reverse("FAQ:edit_settings_bot", kwargs={'bot_id': bot.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'bot_name': 'bot2',
                'status': 'выключен',
                'title_question': 'ok',
                'title_button_row': 4,
                'other_button_row': 4,
                'interval_refresh_base': 33,
                'token': 'qweqweqweqweqweqweqwe23'}
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 302)
        bot_updated = get_object_or_404(SettingsBot, token=data['token'], user=self.user1)
        self.assertEqual(bot.pk, bot_updated.pk)

    def test_edit_settings_bot_another_user(self):
        bot = get_object_or_404(SettingsBot, token='qweqweqweqweqweqweqwe2', user=self.user1)
        url = reverse("FAQ:edit_settings_bot", kwargs={'bot_id': bot.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/account/login/?next=/FAQ/{bot.pk}/settings/")
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        data = {'bot_name': 'bot2',
                'status': 'выключен',
                'title_question': 'ok',
                'title_button_row': 4,
                'other_button_row': 4,
                'interval_refresh_base': 33,
                'token': 'qweqweqweqweqweqweqwe23'}
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 404)
        bot_updated = str(SettingsBot.objects.filter(token=data['token']))
        self.assertEqual(bot_updated, "<QuerySet []>")

    def test_delete_bot(self):
        self.client.force_login(self.user1)
        self.assertEqual(SettingsBot.objects.all().count(), 5)
        bot = get_object_or_404(SettingsBot, token='qweqweqweqweqweqweqwe3', user=self.user1)
        url = reverse("FAQ:delete_bot", kwargs={'bot_id': bot.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(SettingsBot.objects.all().count(), 4)
        bot_deleted = str(SettingsBot.objects.filter(token='qweqweqweqweqweqweqwe3'))
        self.assertEqual(bot_deleted, "<QuerySet []>")

    def test_delete_bot_another_user(self):
        self.client.force_login(self.user2)
        self.assertEqual(SettingsBot.objects.all().count(), 5)
        bot = get_object_or_404(SettingsBot, token='qweqweqweqweqweqweqwe3', user=self.user1)
        url = reverse("FAQ:delete_bot", kwargs={'bot_id': bot.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(SettingsBot.objects.all().count(), 5)
        bot_deleted = str(SettingsBot.objects.filter(token='qweqweqweqweqweqweqwe3'))
        self.assertEqual(bot_deleted, "<QuerySet [<SettingsBot: bot3>]>")

    def test_question_list(self):
        self.client.force_login(self.user1)
        bot = get_object_or_404(SettingsBot, token='qweqweqweqweqweqweqwe2', user=self.user1)
        url = reverse("FAQ:settings_bot_detail", kwargs={'bot_id': bot.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        questions = str(response.context['questions'])
        self.assertEqual(questions,
                         "<QuerySet [<Questions: question4>, <Questions: question3>, <Questions: question2>, <Questions: question1>]>")

    def test_question_list_no_login(self):
        url = reverse("FAQ:settings_bot_detail", kwargs={'bot_id': self.bot1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_create_question(self):
        self.assertEqual(Questions.objects.all().count(), 8)
        self.client.force_login(self.user1)
        url = reverse("FAQ:create_question", kwargs={'bot_id': self.bot1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = {'question': 'question11',
                'answer': 'выключен',
                'general': True,
                '_addanother': 'Сохранить и добавить другой вопрос'
                }
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(Questions.objects.all().count(), 9)
        self.assertTrue(get_object_or_404(Questions, question=data['question'], bot=self.bot1))
        self.assertEqual(response2.url, f"/FAQ/{self.bot1.id}/create_question/")
        data = {'question': 'question12',
                'answer': 'выключен',
                'general': True,
                '_save': 'Сохранить и добавить другой вопрос'
                }
        response3 = self.client.post(url, data)
        self.assertEqual(response3.status_code, 302)
        self.assertEqual(Questions.objects.all().count(), 10)
        self.assertTrue(get_object_or_404(Questions, question=data['question'], bot=self.bot1))
        self.assertEqual(response3.url, f"/FAQ/{self.bot1.id}/")
        data = {'question': 'question13',
                'answer': 'выключен',
                'general': True,
                '_add_sub': 'Сохранить и добавить другой вопрос'
                }
        response4 = self.client.post(url, data)
        self.assertEqual(response4.status_code, 302)
        self.assertEqual(Questions.objects.all().count(), 11)
        question3 = get_object_or_404(Questions, question=data['question'], bot=self.bot1)
        self.assertEqual(response4.url, f"/FAQ/{self.bot1.id}/edit_questions/{question3.id}")

    @staticmethod
    def create_question_post_data(response, new_data=None):
        """Функция создания данных для POST запроса"""
        relations = response.context['formset'].queryset
        relation_count = len(relations)
        data = {'Основной_вопрос-TOTAL_FORMS': relation_count + 3,
                'Основной_вопрос-INITIAL_FORMS': relation_count,
                'Основной_вопрос-MIN_NUM_FORMS': 0,
                'Основной_вопрос-MAX_NUM_FORMS': 1000,
                'csrf_token': response.context['csrf_token'],
                'question': 'question5',
                'answer': 'выключен',
                }
        if new_data is None:
            new_data = {}
        data.update(new_data)
        for i in range(relation_count):
            data.update({f'Основной_вопрос-{i}-id': relations[i].id,
                         f'Основной_вопрос-{i}-base': relations[i].base.id,
                         f'Основной_вопрос-{i}-sub': relations[i].sub.id,
                         })
        return data

    def test_edit_question(self):
        # Тест страница загружена, код 200.
        self.client.force_login(self.user1)
        url = reverse("FAQ:edit_questions", kwargs={'bot_id': self.bot1.id, 'question_id': self.question5.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Тест формы связи - можно выбрать только вопросы текущего бота, остальные не отображаются
        form_select_value_current = str(response.context['formset'][3]['sub'].field.queryset)
        form_select_value_expected = str(Questions.objects.filter(bot=self.bot1.id))
        self.assertEqual(form_select_value_current, form_select_value_expected)
        # Добавление связей вопросов кнопка Сохранить - '_save'
        self.assertEqual(RelationQuestion.objects.all().count(), 2)
        new_data = {'Основной_вопрос-2-base': self.question5.id,
                    'Основной_вопрос-2-sub': self.question8.id,
                    '_save': 'Сохранить',
                    }
        data = self.create_question_post_data(response, new_data)
        # Проверка редиректа при успешной операции
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response2.url, f"/FAQ/{self.bot1.id}/")
        # Проверка сохранения связи в БД
        self.assertEqual(RelationQuestion.objects.all().count(), 3)
        new_relation = RelationQuestion.objects.filter(base=self.question5.id, sub=self.question8.id)
        self.assertTrue(new_relation)
        # Добавление связей вопросов кнопка 'Сохранить и добавить другой вопрос' - '_addanother'
        response = self.client.get(url)
        new_data = {'Основной_вопрос-3-base': self.question5.id,
                    'Основной_вопрос-3-sub': self.question5.id,
                    '_addanother': 'Сохранить и добавить другой вопрос'
                    }
        data = self.create_question_post_data(response, new_data)
        # Проверка редиректа при успешной операции
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response2.url, f"/FAQ/{self.bot1.id}/create_question/")
        # Проверка сохранения связи в БД
        self.assertEqual(RelationQuestion.objects.all().count(), 4)
        new_relation = RelationQuestion.objects.filter(base=self.question5.id, sub=self.question5.id)
        self.assertTrue(new_relation)
        # Удаление связей вопросов кнопка 'Сохранить и продолжить редактирование' - '_continue'
        response = self.client.get(url)
        new_data = {'Основной_вопрос-3-DELETE': True,
                    '_continue': 'Сохранить и продолжить редактирование'}
        data = self.create_question_post_data(response, new_data)
        # Проверка редиректа при успешной операции
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response2.url, url)
        # Проверка удаления из БД
        self.assertEqual(RelationQuestion.objects.all().count(), 3)
        deleted_relation = RelationQuestion.objects.filter(base=data['Основной_вопрос-3-base'],
                                                           sub=data['Основной_вопрос-3-sub'])
        self.assertFalse(deleted_relation)

    def test_edit_question_another_user(self):
        self.assertEqual(RelationQuestion.objects.all().count(), 2)
        # Получаем данные для POST запроса
        self.client.force_login(self.user1)
        url = reverse("FAQ:edit_questions", kwargs={'bot_id': self.bot1.id, 'question_id': self.question5.id})
        response = self.client.get(url)
        new_data = {'Основной_вопрос-3-base': self.question5.id,
                    'Основной_вопрос-3-sub': self.question5.id,
                    '_addanother': 'Сохранить и добавить другой вопрос'
                    }
        data = self.create_question_post_data(response, new_data)
        # Проверка доступа другого пользователя запрос GET
        self.client.force_login(self.user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Проверка доступа другого пользователя запрос POST
        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(RelationQuestion.objects.all().count(), 2)

    def test_delete_question(self):
        self.client.force_login(self.user1)
        self.assertEqual(Questions.objects.all().count(), 8)
        url = reverse("FAQ:delete_question", kwargs={'bot_id': self.bot1.id, 'question_id': self.question5.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(Questions.objects.all().count(), 7)
        question_deleted = str(Questions.objects.filter(question='question5'))
        self.assertEqual(question_deleted, "<QuerySet []>")

    def test_delete_question_another_user(self):
        self.client.force_login(self.user2)
        self.assertEqual(Questions.objects.all().count(), 8)
        url = reverse("FAQ:delete_question", kwargs={'bot_id': self.bot1.id, 'question_id': self.question5.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, 404)
        self.assertEqual(Questions.objects.all().count(), 8)
        question_deleted = str(Questions.objects.filter(question='question5'))
        self.assertEqual(question_deleted, "<QuerySet [<Questions: question5>]>")