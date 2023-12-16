import re, random, string
from smtplib import SMTPException

from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from users import models
from .serializers import(
    CompanySerializer,
    LoginInstructorUserSerializer,
    LoginStudentUserSerializer,
    LoginParentUserSerializer
)

from . import utilities


class GetAllCompanies(APIView):
    authentication_classes = []
    def get(self, request):
        company = models.Company.objects.all()
        serial = CompanySerializer(company, many=True)
        return JsonResponse(serial.data, safe=False)

class GetSignedUpCompanies(APIView):
    authentication_classes = []
    
    def get(self, request):
        company = models.Company.objects.filter(is_sign_up=True)
        serial = CompanySerializer(company, many=True)
        return Response(serial.data)
    
        # return JsonResponse(serial.data, safe=False)

class LoginApi(APIView):
    authentication_classes = []
    
    def post(self, request, *args, **kwargs):
        company_name = kwargs['company_name']
        user_type    = kwargs['user_type']
        
        
        username = request.data.get('username')
        password = request.data.get('password')

        if user_type == 'doctor':
            if models.InstructorAccount.objects.filter(email=username, instructor_type=user_type).exists():

                user_check = models.InstructorAccount.objects.get(email=username)
                user = authenticate(username=user_check.username, password=password)

                if not user.is_active:
                    return Response({'error_active': 'user is not active'}, status=status.HTTP_400_BAD_REQUEST)

                if user is not None:
                    if user.company_name == company_name:
                        serial = LoginInstructorUserSerializer(user)
                        return Response(serial.data)
                    else:
                        return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error_login': 'email or password not correct!'}, status=status.HTTP_400_BAD_REQUEST)


            elif models.InstructorAccount.objects.filter(username=username, instructor_type=user_type).exists():

                user_check = models.InstructorAccount.objects.get(username=username)
                user = authenticate(username=user_check.username, password=password)
                
                if not user.is_active:
                    return Response({'error_active': 'user is not active'}, status=status.HTTP_400_BAD_REQUEST)
                    
                if user is not None:
                    if user.company_name == company_name:
                        serial = LoginInstructorUserSerializer(user)
                        return Response(serial.data)
                    else:
                        return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_login': 'username or password not correct!'}, status=status.HTTP_400_BAD_REQUEST)


            else:
                # return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error_login': 'You can\'t login you arn\'t doctor'}, status=status.HTTP_400_BAD_REQUEST)

        elif user_type == 'assistant':
            if models.InstructorAccount.objects.filter(email=username, instructor_type=user_type).exists():

                user_check = models.InstructorAccount.objects.get(email=username)
                user = authenticate(username=user_check.username, password=password)

                if not user.is_active:
                    return Response({'error_active': 'user is not active'}, status=status.HTTP_400_BAD_REQUEST)

                if user is not None:
                    if user.company_name == company_name:
                        serial = LoginInstructorUserSerializer(user)
                        return Response(serial.data)
                    else:
                        return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_login': 'email or password not correct!'}, status=status.HTTP_400_BAD_REQUEST)


            elif models.InstructorAccount.objects.filter(username=username, instructor_type=user_type).exists():

                user_check = models.InstructorAccount.objects.get(username=username)
                user = authenticate(username=user_check.username, password=password)

                if not user.is_active:
                    return Response({'error_active': 'user is not active'}, status=status.HTTP_400_BAD_REQUEST)

                if user is not None:
                    if user.company_name == company_name:
                        serial = LoginInstructorUserSerializer(user)
                        return Response(serial.data)
                    else:
                        return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error_login': 'username or password not correct!'}, status=status.HTTP_400_BAD_REQUEST)


            else:
                # return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error_login': 'You can\'t login you arn\'t assistant'}, status=status.HTTP_400_BAD_REQUEST)


        elif user_type == 'trainer':
            if models.InstructorAccount.objects.filter(email=username, instructor_type=user_type).exists():

                user_check = models.InstructorAccount.objects.get(email=username)
                user = authenticate(username=user_check.username, password=password)

                if not user.is_active:
                    return Response({'error_active': 'user is not active'}, status=status.HTTP_400_BAD_REQUEST)

                if user is not None:
                    if user.company_name == company_name:
                        serial = LoginInstructorUserSerializer(user)
                        return Response(serial.data)
                    else:
                        return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error_login': 'email or password not correct!'}, status=status.HTTP_400_BAD_REQUEST)


            elif models.InstructorAccount.objects.filter(username=username, instructor_type=user_type).exists():

                user_check = models.InstructorAccount.objects.get(username=username)
                user = authenticate(username=user_check.username, password=password)

                if not user.is_active:
                    return Response({'error_active': 'user is not active'}, status=status.HTTP_400_BAD_REQUEST)

                if user is not None:
                    if user.company_name == company_name:
                        serial = LoginInstructorUserSerializer(user)
                        return Response(serial.data)
                    else:
                        return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error_login': 'username or password not correct!'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                # return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error_login': 'You can\'t login you arn\'t trainer'}, status=status.HTTP_400_BAD_REQUEST)


        elif user_type == 'student':
            if models.StudentAccount.objects.filter(email=username).exists():

                user_check = models.StudentAccount.objects.get(email=username)
                user = authenticate(username=user_check.username, password=password)
                
                if not user.is_active:
                    return Response({'error_active': 'user is not active'}, status=status.HTTP_400_BAD_REQUEST)

                if user is not None:
                    if user.company_name == company_name:
                        serial = LoginStudentUserSerializer(user)
                        return Response(serial.data)
                    else:
                        return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_login': 'email or password not correct!'}, status=status.HTTP_400_BAD_REQUEST)

            elif models.StudentAccount.objects.filter(username=username).exists():

                user_check = models.StudentAccount.objects.get(username=username)
                user = authenticate(username=user_check.username, password=password)
                
                if not user.is_active:
                    return Response({'error_active': 'user is not active'}, status=status.HTTP_400_BAD_REQUEST)

                if user is not None:
                    if user.company_name == company_name:
                        serial = LoginStudentUserSerializer(user)
                        return Response(serial.data)
                    else:
                        return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error_login': 'username or password not correct!'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                # return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error_login': 'You can\'t login you arn\'t student'}, status=status.HTTP_400_BAD_REQUEST)


        elif user_type == 'parent':
            if models.ParentAccount.objects.filter(email=username).exists():

                user_check = models.ParentAccount.objects.get(email=username)
                user = authenticate(username=user_check.username, password=password)

                if not user.is_active:
                    return Response({'error_active': 'user is not active'}, status=status.HTTP_400_BAD_REQUEST)

                if user is not None:

                        serial = LoginParentUserSerializer(user)
                        return Response(serial.data)

                else:
                    return Response({'error_login': 'email or password not correct!'}, status=status.HTTP_400_BAD_REQUEST)
            elif models.ParentAccount.objects.filter(username=username).exists():

                user_check = models.ParentAccount.objects.get(username=username)
                user = authenticate(username=user_check.username, password=password)
                
                if not user.is_active:  
                    return Response({'error_active': 'user is not active'}, status=status.HTTP_400_BAD_REQUEST)
                    
                if user is not None:
                    if user.company_name == company_name:
                        serial = LoginParentUserSerializer(user)
                        return Response(serial.data)
                    else:
                        return Response({'error_login': 'You can\'t login in this company'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_login': 'username or password not correct!'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error_login': 'You can\'t login you arn\'t parent'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error_user_type': 'No chosen correct type'}, status=status.HTTP_400_BAD_REQUEST)
            
        
class SignUpApi(APIView):
    authentication_classes = []
    
    def post(self, request, *args, **kwargs):
        company_name = kwargs['company_name']
        user_type    = kwargs['user_type']
        
        if user_type == 'doctor' or user_type == 'assistant' or user_type == 'trainer':
            username         = request.data.get("username")
            email            = request.data.get("email")
            first_name       = request.data.get("first_name")
            last_name        = request.data.get("last_name")
            department       = request.data.get("department")
            
            password         = request.data.get("password")
            confirm_password = request.data.get("confirm_password")
            
            if utilities.username_exists(username=username):
                return Response({'username_error': 'This username exists!'}, status=status.HTTP_400_BAD_REQUEST)
            
            elif utilities.email_exists(email=email):
                return Response({'email_error': 'This email exists!'}, status=status.HTTP_400_BAD_REQUEST)
            
            expert_password = re.findall("[a-zA-Z]", password)
                
            if len(password) < 8:
                return Response({'error_pass': 'Your password must contain at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)
            elif not expert_password:
                return Response({'error_pass': 'Your password can’t be entirely numeric.'}, status=status.HTTP_400_BAD_REQUEST)
            elif confirm_password != password:
                return Response({'error_pass': 'Your passwords not same!.'}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                user = models.InstructorAccount.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    department=department,
                    company_name=company_name,
                    instructor_type=user_type,
                )
                user.set_password(confirm_password)
                user.is_active = False
                user.save()
                
                return Response({'success': 'Your account created, wait your admin to activate your account.'})
               
        elif user_type == 'student':
            username           = request.data.get("username")
            email              = request.data.get("email")
            first_name         = request.data.get("first_name")
            last_name          = request.data.get("last_name")
            department         = request.data.get("department")
            gender             = request.data.get("gender")
            age                = request.data.get("age")
            national_id        = request.data.get("national_id")
            parent_national_id = request.data.get("parent_national_id")
            parent_email       = request.data.get("parent_email")
            
            password         = request.data.get("password")
            confirm_password = request.data.get("confirm_password")
            
            if utilities.username_exists(username=username):
                return Response({'username_error': 'This username exists!'}, status=status.HTTP_400_BAD_REQUEST)
            
            elif utilities.email_exists(email=email):
                return Response({'email_error': 'This email exists!'}, status=status.HTTP_400_BAD_REQUEST)
            
            expert_password = re.findall("[a-zA-Z]", password)
                
            if len(password) < 8:
                return Response({'error_pass': 'Your password must contain at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)
            elif not expert_password:
                return Response({'error_pass': 'Your password can’t be entirely numeric.'}, status=status.HTTP_400_BAD_REQUEST)
            elif confirm_password != password:
                return Response({'error_pass': 'Your passwords not same!.'}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                try:
                    user = models.StudentAccount.objects.create_user(
                    username           = username,
                    email              = email,
                    first_name         = first_name,
                    last_name          = last_name,
                    company_name       = company_name,
                    department         = department,
                    gender             = gender,
                    age                = age,
                    national_id        = national_id,
                    parent_national_id = parent_national_id
                    )
                    
                    if models.ParentAccount.objects.filter(national_id=parent_national_id).exists():
                        user.set_password(confirm_password)
                        user.is_active = False
                        user.save()
                        return Response({'success': 'Your account created, wait your admin to activate your account.'}, status=status.HTTP_200_OK)
                    else:
                        code = string.ascii_letters
                        for i in range(11):
                            code += str(i)
                        rd = random.choices(code, k=15)
                        
                        user_parent = models.ParentAccount.objects.create_user(
                            username    = user.username+''.join(rd),
                            email       = parent_email,
                            first_name  = 'f_name',
                            last_name   = 'l_name',
                            national_id = parent_national_id
                        )
                        
                        send_mail(
                            'Hi you have now parent account!',
                            f'''
                            This account allows you to lookout your children, follow them,
                            and follow up on their studies continuously,
                            as you can know their grades all the time.
                            
                            You can login with: 
                            username: {user_parent.username}
                            password: {''.join(rd)}
                            ''',
                            'bla@colon.com',
                            [parent_email]
                        )
                        user.set_password(confirm_password)
                        user.is_active = False
                        user.save()
                        
                        user_parent.set_password(''.join(rd))
                        user_parent.is_active = False
                        user_parent.save()
                        
                        return Response({'success': 'Your account created, wait your admin to activate your account.'}, status=status.HTTP_200_OK)
                    
                    
                        
                except SMTPException:
                    return Response({'error_send_mail': 'Failed to create please try again.'}, status=status.HTTP_408_REQUEST_TIMEOUT)
                    
                
                
        



class AuthUser(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    
    def get(self, request):
        user = request.user
        return Response({'user': str(user.email)})