from .models import Strategy, Parameter, Instance, Strategy_type, Time_frame
from rest_framework import serializers
from multiselectfield import MultiSelectField
import json


class Parameter_serializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['parameter_id','id','name','description','variable','add_time','update_time']

        def to_representation(self, instance):
            data = super().to_representation(instance)
            parameter = json.loads(data['parameter'])
            data['parameter'] = parameter
            return data

class Strategy_serializer(serializers.ModelSerializer):
    #parameters = Parameter_serializer(many=True)
    class Meta:
        model = Strategy
        fields = ['strategy_id','name','code','type','script','parameter','add_time','update_time']

class Instance_serializer(serializers.ModelSerializer):
    initialize_day = serializers.MultipleChoiceField(choices=Instance.Days)
    class Meta:
        model = Instance
        fields = ['strategy_fk', 'symbol', 'initialize_day', 'initialize_time', 'terminate_time','add_time','update_time','name']
        read_only_fields = ['name']




class Strategy_type_serializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy_type
        fields = ['strategy_type']

class Time_frame_serializer(serializers.ModelSerializer):

    class Meta:
        model = Time_frame
        fields = ['time_frame','strategy_type']