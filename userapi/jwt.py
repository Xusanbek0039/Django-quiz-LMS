from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
import jwt

from users import models


class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        
        auth_data = auth_header.decode('utf-8')
        
        auth_token = auth_data.split(" ")
        print(auth_data)
        
        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed('Token not valid.')
        
        token = auth_token[1]
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            
            username = payload['username']
            
            try:
                
                user = models.SuperUserAccount.objects.get(username=username)
                return (user, None)
                
            except models.SuperUserAccount.DoesNotExist as ex:
                pass
            
            try:
                
                user = models.AdminAccount.objects.get(username=username)
                return (user, None)
                
            except models.AdminAccount.DoesNotExist as ex:
                pass
            
            try:
                
                user = models.InstructorAccount.objects.get(username=username)
                return (user, None)
                
            except models.InstructorAccount.DoesNotExist as ex:
                pass
            
            try:
                
                user = models.StudentAccount.objects.get(username=username)
                return (user, None)
                
            except models.StudentAccount.DoesNotExist as ex:
                pass
            
            try:
                
                user = models.ParentAccount.objects.get(username=username)
                return (user, None)
                
            except models.ParentAccount.DoesNotExist as ex:
                pass
            
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed('Token is expired, login again')
        
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed('Token is invalid')
        
        # except models.SuperUserAccount.DoesNotExist as ex:
        #     raise exceptions.AuthenticationFailed('No such user')
        
        