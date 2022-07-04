from .forms import SettingsBotForm
from .models import Questions, RelationQuestion, SettingsBot
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.core.exceptions import (
    FieldDoesNotExist, FieldError, PermissionDenied, ValidationError,
)

# from access.admin import *


class AccessUserAdmin(UserAdmin):
    list_editable = ['email']

    def get_list_display(self, request):
        fields = super(AccessUserAdmin, self).get_list_display(request) or []
        if request.user.is_superuser:
            return fields
        return list(set(fields).difference(['password', 'email']))

    def _fieldsets_exclude(self, fieldsets, exclude):
        ret = []
        for nm, params in fieldsets:
            if not 'fields' in params:
                ret.append((nm, params))
                continue
            fields = []
            for f in params['fields']:
                if not f in exclude:
                    fields.append(f)
            pars = {}
            pars.update(params)
            pars['fields'] = fields
            ret.append((nm, pars))
        return ret

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super(AccessUserAdmin, self).get_fieldsets(request, obj)) or []
        if request.user.is_superuser:
            return fieldsets
        if not obj:
            return fieldsets
        if obj.pk != request.user.pk:
            return self._fieldsets_exclude(fieldsets, ['password', 'email'])
        return self._fieldsets_exclude(fieldsets, ['is_superuser'])


class RelationQuestionInline(admin.TabularInline):
    """Дочерние вопросы"""
    model = RelationQuestion
    fk_name = "base"


class QuestionsAdmin(admin.ModelAdmin):
    """Форма для создания/редактирования вопросов"""
    list_display = ('question', 'answer', 'general', 'bot', 'updated',)
    list_filter = ('bot',)
    list_editable = ('general', 'bot')
    inlines = (RelationQuestionInline,)

    def get_inlines(self, request, obj):
        if obj:
            return self.inlines
        else:
            return []

    def get_fields(self, request, obj=None):
        fields = list(super(QuestionsAdmin, self).get_fields(request, obj))
        exclude_set = set()
        if obj:  # obj will be None on the add page, and something on change pages
            exclude_set.add('bot')
        return [f for f in fields if f not in exclude_set]


    # def get_fields(self, request, obj=None):
    #     if self.fields:
    #         return self.fields
    #     form = self._get_form_for_get_fields(request, obj)
    #     return [*form.base_fields, *self.get_readonly_fields(request, obj)]

    # def get_relation(self, obj):
    #     if obj:
    #         # inlines=(RelationQuestionInline,)
    #         return 'bot'


class SettingBotAdmin(admin.ModelAdmin):
    """Настройки ботов"""
    list_display = ('bot_name', 'id', 'created', 'user', 'status')
    # exclude = ['user']
    # list_editable = ('user',)
    list_filter = ('user',)
    form = SettingsBotForm


    def save_model(self, request, obj, form, change):
        """Автоматически назначаем автора записи"""
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

    # def get_queryset(self, request):
    #     """Ограничиваем видимость записей только для автора"""
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(id=request.user.id)


admin.site.register(Questions, QuestionsAdmin)
admin.site.register(SettingsBot, SettingBotAdmin)
