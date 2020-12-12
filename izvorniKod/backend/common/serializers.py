from datetime import datetime

from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from common.models import User, Post, Laundry
from rest_framework.serializers import ModelSerializer


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `only_fields` argument that
    controls which fields should be displayed.
    """
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('only_fields', None)
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        if data.get('password') is not None:
            try:
                password_validation.validate_password(data.get('password'))
            except Exception as error:
                raise serializers.ValidationError(error)
        if data.get('JMBAG') is not None and len(data.get('JMBAG')) != 10:
            raise serializers.ValidationError(' JMBAG length must be exactly 10!')
        return data

    def create(self):
        obj = User.objects.create_user(**self.validated_data)
        return obj

    def update(self, obj, validated_data):
        if 'password' in validated_data:
            obj.password = make_password(validated_data.get('password'))
        if 'username' in validated_data:
            obj.username = validated_data.get('username')
        obj.save()
        print(obj.first_name)
        return obj


class PostSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        

class LaundrySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Laundry
        exclude = ['date_changed']

    def validate(self, data):
        if data.get('pause_start') is not None and data.get('pause_start').minute >= 30:
            raise serializers.ValidationError('Pauza mora završiti prije novog termina!!!')
        return data
