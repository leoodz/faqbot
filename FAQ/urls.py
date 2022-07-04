from django.urls import path

from .views import *

urlpatterns = [
    # FAQ views
    path('', bot_list, name='bot_list'),
    path('create_bot/', BotCreateView.as_view(), name='create_bot'),
    path('<int:bot_id>/settings/', edit_settings_bot, name='edit_settings_bot'),
    path('<int:bot_id>/delete_bot/', BotDeleteView.as_view(), name='delete_bot'),
    path('<int:bot_id>/', SettingsBotDetail.as_view(), name='settings_bot_detail'),

    path('<int:bot_id>/create_question/', QuestionCreateView.as_view(), name='create_question'),
    path('<int:bot_id>/edit_questions/<int:question_id>', edit_question, name='edit_questions'),
    path('<int:bot_id>/delete_question/<int:question_id>', QuestionDeleteView.as_view(), name='delete_question'),
    ]