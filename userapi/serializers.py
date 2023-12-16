from users import models
from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ['id', 'company_name', 'admins_number',
                  'instrauctors_number', 'students_number',
                  'start', 'end', 'is_sign_up', 'contact_email',
                  'description'
                  ]


class LoginInstructorUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = models.InstructorAccount
        fields = ['password', 'token']

        read_only_fields = ['token']


class LoginStudentUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = models.StudentAccount
        fields = ['password', 'token']

        read_only_fields = ['token']


class LoginParentUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = models.ParentAccount
        fields = ['password', 'token']

        read_only_fields = ['token']