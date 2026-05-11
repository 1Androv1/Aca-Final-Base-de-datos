from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class MyUserManager(BaseUserManager):
	def create_user(self, email, name, password=None):
		is_first_user = self.model.objects.count() == 0
		my_user = self.model(
			email=self.normalize_email(email),
			name=name,
			is_admin=is_first_user,
		)
		my_user.set_password(password)
		my_user.save()
		return my_user


class MyUser(AbstractBaseUser):
	email = models.EmailField(max_length=150, unique=True)
	name = models.CharField(max_length=100, blank=True)
	is_admin = models.BooleanField(default=False)
	objects = MyUserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']


