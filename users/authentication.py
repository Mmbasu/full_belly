from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class InactiveModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
