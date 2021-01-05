from django.db import models
from django.conf import settings
""""
Used to extend the abstractBaseUser class in django and the permissionMixin are used to use the permission class 
attributes such as is_staff and is_active
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# used to derive and extend the BaseUserManger holding user information
from django.contrib.auth.base_user import BaseUserManager
# used for text translation but generally not required unless the end user wants it
from django.utils.translation import gettext_lazy as _


"""
UserCreator Class 
This class is used to extend the base user module in django and add the necessary fields of the user 
It has 
    base_user  : It is used to validate and save the user instance from the create_user and create_superuser 
    classes 
    
    create_user : It is used to create user along with extra fields which are 
    is_staff and is_superuser which specifies the permission to the user
    
    create_superuser : It is used to create admins or superuser with extra fields as specified above
"""


class UserCreator(BaseUserManager):

    def base_user(self, name, username, email, password, **args):
        user = self.model(name=name, username=username, email=self.normalize_email(email), **args)
        user.set_password(password)
        user.full_clean()
        user.save()
        return user

    def create_user(self, name, username, email, password, **args):
        args.setdefault('is_staff', False)
        args.setdefault('is_superuser', False)
        return self.base_user(name, username, email, password, **args)

    def create_superuser(self, name, username, email, password, **args):
        args.setdefault('is_staff', True)
        args.setdefault('is_superuser', True)

        if args.get('is_staff') is not True:
            raise ValueError('User does not have staff priviledges')
        return self.base_user(name, username, email, password, **args)



"""
Model User 
Contains the following attributes as mentioned below 
contains objects as object to UserCreator 
"""


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email_address'), unique=True)
    date_of_birth = models.DateField(_('date_of_birth'))
    country = models.CharField(_("country"),null = False ,max_length = 30)
    city = models.CharField(_("city"),null = False ,  max_length = 30)
    username = models.CharField(_('username'), unique=True, max_length=100)
    gender = models.CharField(_('gender'), null = False,  max_length=100)
    partner_gender = models.CharField(_('partner_gender'),null = False, max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email' , 'date_of_birth' , 'gender' , 'country' , 'partner_gender' , 'city']
