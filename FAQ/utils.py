from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from .models import *


class AuthorFilterMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        bot = get_object_or_404(SettingsBot, id=self.kwargs['bot_id'], user=self.request.user)
        return super().dispatch(*args, **kwargs, bot=bot)


class CheckLoginMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)