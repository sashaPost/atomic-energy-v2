from rest_framework import serializers
from .models import *
import logging



logger = logging.getLogger(__name__)

class NullToFalseBaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(NullToFalseBaseSerializer, self).to_representation(instance)
        
        logger.info(f"'data.items()': {data.items()}")
        
        for key, value in data.items():
            
            logger.info(f"'key': {key}")
            logger.info(f"'value': {value}")
            
            if isinstance(value, dict):
                logger.info(f"!!! 'if isinstance(value, dict)' was triggered !!!")
                self.replace_null_values(value)
            elif value is None:
                logger.info(f"!!! 'elif value is None' was triggered !!!")
                data[key] = False
        return data

    def replace_null_values(self, data):
        """Recursively replaces Null values with False"""
        for key, value in data.items():
            if isinstance(value, dict):
                self.replace_null_values(value)
            elif value is None:
                data[key] = False

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

# class ProcuringEntitySerializer(serializers.ModelSerializer):
class ProcuringEntitySerializer(NullToFalseBaseSerializer):
    class Meta:
        model = ProcuringEntity
        fields = '__all__'
        
class ValueSerializer(NullToFalseBaseSerializer):
    class Meta:
        model = Value
        fields = '__all__'
        
class ItemSerializer(NullToFalseBaseSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        
class TenderPeriodSerializer(NullToFalseBaseSerializer):
    class Meta:
        model = TenderPeriod
        fields = '__all__'
        
class TenderStepSerializer(NullToFalseBaseSerializer):
    class Meta:
        model = TenderStep
        fields = '__all__'

class ProcurementSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='procurement-detail',
        lookup_field='pk',
    )
    unit = UnitSerializer(read_only=True)
    procuring_entity = ProcuringEntitySerializer(read_only=True)
    value = ValueSerializer(read_only=True)
    item = ItemSerializer(read_only=True)
    tender_period = TenderPeriodSerializer(read_only=True, source='period')
    tender_step = TenderStepSerializer(read_only=True, source='step')
        
    class Meta:
        model = Procurement
        fields = '__all__'
        ordering = ['-date']
        
    def to_representation(self, instance):
        data = super(ProcurementSerializer, self).to_representation(instance)
        
        if data['file']:
            data['file'] = data['file'].replace('tested', 'new')
        
        # logger.info(f"Procurement: {str(instance)}")
        # logger.info(f"Item: {str(instance.item)}")
        # logger.info(f"Tender Period: {str(instance.period)}")
        # logger.info(f"Tender Step: {str(instance.step)}")
        # logger.info(f"Raw Data: {data}")
        
        return data