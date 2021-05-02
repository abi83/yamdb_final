from uuid import uuid1

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db import models
from django.db.models import signals
from django.dispatch import receiver


class YamdbUserManager(BaseUserManager):
    """
    Custom User Manager for custom User model.
    Provides correct implementation of 'manage.py createsuperuser' command
    """

    def create_superuser(self, username=None, password=None, email=None):
        user_obj = self.create_user(
            username=str(uuid1()),
            email=email,
            password=password,
            is_staff=True,
            is_admin=True,
            is_active=True,
        )
        return user_obj

    def create_user(self, email,
                    username,
                    password=None,
                    is_active=True,
                    is_staff=False,
                    is_admin=False,
                    ):
        if not email:
            raise ValueError('User must have an email address')
        user_obj = self.model(
            email=email
        )
        user_obj.set_password(password)
        user_obj.username = username
        user_obj.email = email
        user_obj.is_staff = is_staff
        user_obj.is_superuser = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj


class YamdbUser(AbstractUser):
    """
    Custom User model. No username or password requires for registration.
    Register via email, confirm email via confirmation code and
    authorise with JWT token.
    Roles are different from Django Groups. Admins can manage users,
    Moderators can manage content, Users can publish content.
    """

    class Role(models.TextChoices):
        USER = ('usr', 'user')
        MODERATOR = ('mod', 'moderator')
        ADMIN = ('adm', 'admin')

    bio = models.TextField(max_length=255, blank=True,
                           verbose_name='Users biography')
    role = models.CharField(max_length=10, default=Role.USER,
                            choices=Role.choices)
    email = models.EmailField(unique=True, db_index=True, blank=False,
                              null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = YamdbUserManager()

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Yamdb User'
        verbose_name_plural = 'Yamdb Users'

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN


@receiver(signals.post_save, sender=YamdbUser)
def send_confirmation_code(sender, instance, created, **kwargs):
    """
    Sends email with confirmation code for Users activation
    """
    code = default_token_generator.make_token(instance)
    if created:
        email = EmailMessage(
            subject='YamDB confirmation code',
            body=f'Your confirmation code: {code}',
            to=[f'{instance.email}', ],
        )
        email.send()
