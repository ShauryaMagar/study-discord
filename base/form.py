from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model=Room #specify the model for which form is to be made
        fields = '__all__' #specify the fields. Using __all__ creates a form for all the mentioned fields