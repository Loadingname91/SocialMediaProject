from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
"""
Class UserCreationForm 
This class is extending the build in form class in authentication forms 
It is used to create users using the admin interface
"""

class UserCreationForm(UserCreationForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta(UserCreationForm):
        model = User
        fields = ('username',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

"""
Class UserChangeForm  
This class is extending the build in form class in authentication forms 
It is used to change users information using the admin interface
"""

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('username','name', 'email' , 'date_of_birth' , 'gender' , 'country' , 'partner_gender' , 'city', 'password')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


"""
Class UserAdmin  
This class extends UserAdmin and it creates add and change from derived from the respective imports
It also holds list and list filter display for sorting through the list of users
"""


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ( 'username','email','is_active',"gender","partner_gender",'city','country')
    list_filter = ('is_active',"gender","partner_gender",'city','country')
    fieldsets = (
        (None, {'fields': ('username','name', 'email' , 'date_of_birth' , 'gender' , 'country' , 'partner_gender' , 'city' , 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )
    search_fields = ('username',"name","email")


admin.site.register(User,UserAdmin)
