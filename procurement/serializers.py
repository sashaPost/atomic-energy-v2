from rest_framework import serializers
from .models import *



class ProcurementSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Procurement
        fields = '__all__'