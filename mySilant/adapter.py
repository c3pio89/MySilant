from django.conf import settings

from allauth.account.adapter import DefaultAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        """
        Разрешаем/запрещаем регистрацию с помощью переменной ACCOUNT_ALLOW_SIGNUPS в settings
        """
        allow_signups = super(CustomAccountAdapter, self).is_open_for_signup(request)
        # По умолчанию используется значение super
        return getattr(settings, 'ACCOUNT_ALLOW_SIGNUPS', allow_signups)