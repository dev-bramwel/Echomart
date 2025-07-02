from rest_framework import serializers
from django.contrib.auth.models import User
from .models import AccountVendor  # ✅ Renamed model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  

    def create(self, validated_data):  # type: ignore
        return User.objects.create_user(**validated_data) # type: ignore

class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AccountVendor  # ✅ Use renamed model
        fields = ['user', 'shop_name', 'phone', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):  # type: ignore
        user_data = validated_data.pop('user') # type: ignore
        user = User.objects.create_user(**user_data) # type: ignore
        vendor = AccountVendor.objects.create(user=user, **validated_data)
        return vendor

