#it converts python object into JSON. When sending the data from db, it converts to JSON
from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model= Room
        fields = '__all__'
