from statistics import mode
from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model=Room #specify the model for which form is to be made
        fields = '__all__' #specify the fields. Using __all__ creates a form for all the mentioned fields
        exclude = ['host', 'participants'] #excludes the named table columns from form

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']