from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    # write_only=True ensures the password isn't sent back in the response
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Remove confirm_password before creating the user
        validated_data.pop('confirm_password')
        # Use create_user (which you should have in your Manager) to hash the password
        user = CustomUser.objects.create_user(**validated_data)

        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # Fields that the user is allowed to see and update
        fields = ['id', 'first_name', 'last_name', 'email', 'bio', 'created_at']
        # Email and ID should usually be read-only in a profile update
        read_only_fields = ['id', 'email', 'created_at']