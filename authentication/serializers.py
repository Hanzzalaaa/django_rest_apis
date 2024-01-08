from  django.contrib.auth.models import User
from rest_framework import serializers, status
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
# from .utils import  create_firebase_profile, get_firestore_id, signin_firebase
import uuid,random
from django.db import transaction
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
        


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields["username"] = serializers.CharField(required = True)
        self.fields["password"] = serializers.CharField(required = True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        try:
            user_obj = User.objects.get(Q(email=username)|Q(username=username))
        except User.DoesNotExist as e:
            user_obj =  None
        if user_obj is not None:
            authenticate_kwargs = {
                "username": user_obj.username,
                "password": password,
            }
            print("authenticate_kwargs",authenticate_kwargs)
            try:
                authenticate_kwargs["request"] = self.context["request"]
            except KeyError:
                pass

            self.user = authenticate(**authenticate_kwargs)
            print("self.user", self.user)
            if not api_settings.USER_AUTHENTICATION_RULE(self.user):
                return {'message': 'Invalid password'}
            else:
                data = {
                    'email' : self.user.email
                }
                return data 
        else:
            return {'message': 'Invalid email or username'}
        
        return  {}
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)


class CustomTokenObtainPairSerializer(MyTokenObtainPairSerializer):
    token_class = RefreshToken
    def validate(self, attrs):
        response = {"status" : False,"status_code"  : None, "message" : None, "data" : None}
        data = super().validate(attrs)
        if 'message' not in data.keys():
            print(data)
            refresh = self.get_token(self.user)
            response["status"] = True
            
            response["status_code"] = status.HTTP_200_OK
            response["message"] = "Login Successfully"
            response["data"] = data
            response['data']["refresh"] = str(refresh)
            response['data']["access"] = str(refresh.access_token)
            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, self.user)
        else:
            response["status"] = False
            response["message"] = data["message"]
            response["status_code"] = status.HTTP_400_BAD_REQUEST
        return response

    





class RegisterSerializer(serializers.Serializer):
    token_class = RefreshToken
    status_code = serializers.IntegerField(read_only = True,default =status.HTTP_400_BAD_REQUEST)
    status = serializers.BooleanField(read_only=True,default=False)
    message = serializers.CharField(read_only=True,default =None)
    data = serializers.DictField(read_only=True,default = None)
    
    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resp = {'status' : False,'status_code' : status.HTTP_400_BAD_REQUEST,'message': None,'data' : None}
        self.fields['full_name'] = serializers.CharField(max_length= 100, required = True,write_only=True)
        self.fields['email'] = serializers.EmailField(required=True,write_only=True) #,validators=[UniqueValidator(queryset=User.objects.all())]
        self.fields['password'] = serializers.CharField(write_only=True, required=True)#, validators=[cus_password_validator]
        self.fields['confirm_password'] = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        errors = None
        password = attrs['password']
        password2 = attrs['confirm_password']
        # phone_number = attrs['phone_number']
        email = attrs['email']
        attrs['valid'] = False
        special_characters = r'!"\#$%&()*+,-./:;<=>?@[\\]^_`{|}~\'•√π÷×§∆£¢€¥°©®™✓'

        if User.objects.filter(email=email).exists():
            errors = "This email is already taken."

        if password != password2:
            errors = "Password fields didn’t match."
        if not any(char.islower() for char in password):
            errors = "Password must contain at least one lowercase letter."
        if not any(char.isupper() for char in password):
            errors = "Password must contain at least one uppercase letter."
        if not any(char in special_characters for char in password):
            errors = "Password must contain at least one Special character."

        if errors is None:
            attrs['valid'] = True
        else:
            attrs['error'] = errors
        return attrs
    
    def create(self, validated_data):
        print("validated_data:", validated_data)
        if validated_data['valid'] == True:
            first_name = validated_data['full_name']
            # phone_number = validated_data['phone_number']
            username = None
            loop_status = True
            i = 100
            while loop_status:
                username = first_name.replace(" ", "").lower() + str(random.randint(1, i))
                obj = User.objects.filter(username=username).first()
                if obj is None:
                    loop_status = False
                else:
                    i += i
            with transaction.atomic():
                user_obj = User.objects.create(
                    username=username,
                    email=validated_data['email'],
                    first_name=first_name,
                )
                print("user_obj:", user_obj)
                user_obj.set_password(validated_data['password'])
                user_obj.save()
                refresh = self.get_token(user_obj)
                self.resp['status'] = True 
                self.resp['status_code'] = status.HTTP_201_CREATED
                self.resp['message'] = 'User created successfully'
                self.resp["data"] ={
                "access" : str(refresh.access_token),"refresh" :  str(refresh),
                "full_name" : first_name, "email" : validated_data['email'] }
        else:
            self.resp['message'] = validated_data.get('error')
            print("Response: %s" % self.resp)
        return self.resp







