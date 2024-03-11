from .models import Cobots
from rest_framework import serializers

class CobotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cobots
        fields = ('pk', 'event', 'place', 'name', 'is_approved', 'user_chat_id')

