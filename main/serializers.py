from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields="__all__"



class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=Record
        fields="__all__"

    def validate_client(self,client):
        if client.debt > 500000:
            raise serializers.ValidationError("Maxsulot olib ketishingiz mumkin emas")
        return client

