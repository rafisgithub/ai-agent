from .models import UserInformation
from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password



class UploadCvSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = ['id', 'custom_user','cv_file']
        read_only_fields = ['custom_user']



        
   
