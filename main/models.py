from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .choices import (languages, countries)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    email = models.EmailField('email address', unique=True)
    objects = UserManager()


class Billing(models.Model):
    user = models.ForeignKey('User', related_name='billings', on_delete=models.CASCADE)
    company = models.CharField('Ընկերություն', max_length=200, blank=True, null=True)
    country = models.CharField('Երկիր', choices=countries, max_length=200)
    address1 = models.CharField('Հասցե 1-ին', max_length=200)
    address2 = models.CharField('Հասցե 2-րդ', max_length=200, blank=True, null=True)
    city = models.CharField('Քաղաք', max_length=200)
    county = models.CharField('Մարզ', max_length=200, blank=True, null=True)
    postcode = models.CharField('Փոստային ինդեքս', max_length=10)
    phone = models.CharField('Հեռախոսահամար', max_length=16)
    is_active = models.BooleanField('Ակտի՞վ է', default=False)
    created_at = models.DateTimeField('Ստեղծվել է', auto_now_add=True)
    updated_at = models.DateTimeField('Փոփոխվել է', auto_now=True)

    class Meta:
        verbose_name = 'Վճարման տվյալ'
        verbose_name_plural = 'Վճարման տվյալներ'
