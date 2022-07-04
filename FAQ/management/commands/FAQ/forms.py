from django.forms import ModelForm, PasswordInput, TextInput, NumberInput, CharField, ModelChoiceField
from django.forms.widgets import Select, Textarea, CheckboxInput

from FAQ.models import SettingsBot, RelationQuestion, Questions


class SubQuestionForm(ModelForm):
    """Показывает вопросы выбранного бота"""
    sub = CharField(widget=Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        self.queryset_for_choices = kwargs.pop('queryset_for_choices', None)
        super(SubQuestionForm, self).__init__(*args, **kwargs)
        self.fields['sub'] = ModelChoiceField(self.queryset_for_choices, label="Дополнительный вопрос",
                                              empty_label="Не выбран")

    class Meta:
        model = RelationQuestion
        fields = ['sub']
        widgets = {'sub': Select(attrs={'class': 'form-select'}), }


class QuestionsForm(ModelForm):
    class Meta:
        model = Questions
        fields = ['question',
                  'answer',
                  'general',
                  ]
        widgets = {'question': TextInput(attrs={'class': 'form-control'}),
                   'answer': Textarea(attrs={'class': 'form-control'}),
                   'general': CheckboxInput(attrs={'class': 'form-check-input ml-0'})}


class SettingsBotForm(ModelForm):
    class Meta:
        model = SettingsBot
        fields = ['bot_name',
                  'token',
                  'title_question',
                  'title_button_row',
                  'other_button_row',
                  'interval_refresh_base',
                  ]
        widgets = {'token': PasswordInput(render_value=True, attrs={'class': 'form-control'}),
                   'title_question': Textarea(attrs={'class': 'form-control'}),
                   'bot_name': TextInput(attrs={'class': 'form-control'}),
                   'title_button_row': NumberInput(attrs={'class': 'form-control'}),
                   'other_button_row': NumberInput(attrs={'class': 'form-control'}),
                   'interval_refresh_base': NumberInput(attrs={'class': 'form-control'}),
                   }
