from rest_framework import serializers
from .models import Vendor, VendorBankDetails


class VendorBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorBankDetails
        fields = [
            'id', 'bank_name', 'account_name', 'account_number', 'routing_number',
            'is_default', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VendorSerializer(serializers.ModelSerializer):
    bank_details = VendorBankDetailsSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Vendor
        fields = [
            'id', 'user', 'business_name', 'business_description', 'business_logo',
            'business_address', 'business_phone', 'business_email', 'website',
            'is_verified', 'is_active', 'bank_details', 'created_at', 'updated_at'
        ]
        
        read_only_fields = ['id', 'user', 'is_verified', 'created_at', 'updated_at']
        

class VendorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'business_name', 'business_description', 'business_logo',
            'business_address', 'business_phone', 'business_email', 'website'
        ]
        
    def validate(self, data):
            user = self.context['request'].user
            if Vendor.objects.filter(user=user).exists():
                raise serializers.ValidationError("You already have a vendor profile.")
            return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class VendorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'business_name', 'business_description', 'business_logo',
            'business_address', 'business_phone', 'business_email', 'website', 'is_active'
        ]


class CreateBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorBankDetails
        fields = [
            'bank_name', 'account_name', 'account_number', 'routing_number', 'is_default'
        ]

    def create(self, validated_data):
        validated_data['vendor'] = self.context['vendor']
        
        # If this is set as default, unset all other defaults for this vendor
        if validated_data.get('is_default', False):
            VendorBankDetails.objects.filter(
                vendor=validated_data['vendor']
            ).update(is_default=False)
        
        return super().create(validated_data)
