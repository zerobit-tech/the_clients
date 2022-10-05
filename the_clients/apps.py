from django.apps import AppConfig


class TheEnvironmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'the_clients'

    def ready(self):
        from the_user.decorators import register_auth_method
        from .models import Client

        @register_auth_method
        def auth_by_token(request,token):
            return Client.get_client_by_token(token)