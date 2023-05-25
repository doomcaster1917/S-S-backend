import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.db import models

class UserManager(BaseUserManager):
    """
    Django требует, чтобы кастомные пользователи определяли свой собственный
    класс Manager. Унаследовавшись от BaseUserManager, мы получаем много того
    же самого кода, который Django использовал для создания User (для демонстрации).
    """

    def create_user(self, user_id, first_name, last_name, avatar_url, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if user_id is None:
            raise TypeError('Users must have a user_id(instead username).')

        user = self.model(user_id=user_id, first_name=first_name, last_name=last_name, avatar_url=avatar_url)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, user_id, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(user_id, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):

    user_id = models.IntegerField(db_index=True, unique=True, default=False)
    first_name = models.CharField(max_length=255, default=False)
    last_name = models.CharField(max_length=255, default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar_url = models.CharField(db_index=True, max_length=455, default=False)

    # Дополнительный поля, необходимые Django
    # при указании кастомной модели пользователя.
    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'user_id'
    # REQUIRED_FIELDS = ['username']

    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()

    def __str__(self):
        """ Строковое представление модели (отображается в консоли) """
        return f'{self.first_name} {self.last_name} * {self.user_id}'

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.first_name

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': self.pk,
            'exp': dt
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
