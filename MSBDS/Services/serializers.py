# serializers.py

from rest_framework import serializers
from .models import Farmer

class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ['name', 'gender', 'date_of_birth', 'password', 'location', 'contact']
