from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin, Group, Permission
from django.db import models




class PersonManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email_address, password=None, **extra_fields):
        if not email_address:
            raise ValueError("The Email field must be set")
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email_address, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, help_text="Name of the Author")
    email_address = models.EmailField(max_length=100, unique=True, help_text="Email of the person")
    age = models.IntegerField()
    profile_pic=models.ImageField(upload_to='images/',null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = PersonManager()

    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ['name','age']  # Add other required fields for user creation

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email_address