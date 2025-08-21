from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password1 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = (
            'email','first_name', 'last_name',
            'password', 'password1', 
            'user_type', 
        )
        extra_kwargs = {
            'email': {'help_text': 'Required. Enter a valid email address.'},
            'user_type': {'help_text': 'Select account type: customer or seller.'},
            # 'password' : {'write_only': True},
        }
    
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()
    
    
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({
                'password1': "Password confirmation doesn't match password."
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password1')
        user = User.objects.create_user(**validated_data)
        return user

class UserAuthenticationSerializer(serializers.Serializer):
    email = serializers.CharField(max_length =255)    
    password = serializers.CharField(min_length  = 8,write_only= True)  
    full_name = serializers.CharField(max_length = 255,read_only = True)
    refresh_token = serializers.CharField(max_length = 255,read_only = True)
    access_token = serializers.CharField(max_length = 255,read_only = True)
    
    # class Meta:
    #     fields =('email','password','full_name','access_token','refresh_token')
        
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request,email =email ,password =password)
        if user is None :
            raise AuthenticationFailed('Crendienatial does not match')
        user_token = user.get_tokens()
        
        return {
            'email' : user.email,
            'full_name' : user.full_name ,
            'access_token' : str(user_token.get('access')),
            'refresh_token' : str(user_token.get('refresh'))
        } 
    
class UserLogoutSerilaizers(serializers.Serializer):
    refresh= serializers.CharField()   
    
    default_error_messages = {
        'bad_token': 'Token is invalid or expired'
    }

    
    def validate(self, attrs):
        self.token = attrs.get('refresh')
        return   attrs
    def save(self, **kwargs):
        try :
            token = RefreshToken(self.token)
            token.blacklist()
        except  TokenError  :
            raise self.fail('bad_token')
    


 
