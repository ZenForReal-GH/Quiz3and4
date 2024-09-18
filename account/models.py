from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password, is_staff=True)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password, is_staff=True, is_admin=True)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active



