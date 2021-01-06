from authentication.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from authentication.utils.email_validation import Email_domain_validator


"""
class RegisterSerializer
Used to register using the following fields as mentioned below 
"""


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all()),Email_domain_validator]
            )

    class Meta:
        model = User
        fields = ('name','username' ,'email' , 'date_of_birth' , 'gender' , 'country' , 'partner_gender' , 'city' ,"is_staff","is_active",'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data["name"],
            username=validated_data["username"],
            email=validated_data["email"],
            date_of_birth = validated_data["date_of_birth"],
            city = validated_data["city"],
            country = validated_data['country'],
            gender = validated_data['gender'],
            partner_gender = validated_data['partner_gender'],
            password= validated_data['password']
        )
        user.save()
        return user




class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'name', 'email')

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.name = validated_data['name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance
