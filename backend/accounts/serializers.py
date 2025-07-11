from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, UserProfile

# Serializer for displaying and updating user profile data
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'address', 'city', 'country', 'postal_code']


# Main serializer for outputting full user info
class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'full_name', 'phone_number',
            'date_of_birth', 'is_vendor', 'profile', 'password', 'created_at'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


# Serializer for registering new users

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone_number', 'password']


    def create(self, validated_data):
        password = validated_data.pop('password')

        full_name = " ".join(validated_data.pop('full_name').strip().split())  # Normalize spacing

        user = CustomUser.objects.create_user(
            full_name=full_name,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user



# Serializer for login authentication
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Both email and password are required.')

        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if not user:
            raise serializers.ValidationError({'detail': 'Invalid email or password.'})
        if not user.is_active:
            raise serializers.ValidationError({'detail': 'User account is disabled.'})

        attrs['user'] = user
        return attrs


# Serializer for updating user profile (e.g., from frontend)
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'address', 'city', 'country', 'postal_code']
        
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'phone_number', 'date_of_birth']

    def validate_username(self, value):
        if value == '':
            return None  # treat blank as null

        user = CustomUser.objects.filter(username=value).exclude(id=self.instance.id).first()
        if user:
            raise serializers.ValidationError("This username is already taken.")
        return value


# Serializer for updating CustomUser fields
class CustomUserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'phone_number', 'date_of_birth']

    def validate_username(self, value):
        if value == '':
            return None  # treat blank as null

        user = CustomUser.objects.filter(username=value).exclude(id=self.instance.id).first()
        if user:
            raise serializers.ValidationError("This username is already taken.")
        return value


# Serializer for changing password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match")
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
