from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
import jwt, datetime
from django.conf import settings


class SuperUserAccountManager(BaseUserManager):
    
    def create_user(self, username, email, first_name, last_name, password=None):
        user = self.model(
            username   =username,
            email      =self.normalize_email(email),
            first_name =first_name,
            last_name  =last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, first_name, last_name, password):
        user = self.create_user(
            username   =username,
            email      =self.normalize_email(email),
            first_name =first_name,
            last_name  =last_name,
            password   =password
        )
        
        user.save(using=self._db)
        return user

class SuperUserAccount(AbstractBaseUser):
    username          = models.CharField(max_length=50, unique=True)
    email             = models.EmailField(max_length=50, unique=True)
    date_joined       = models.DateTimeField(auto_now_add=True)
    last_login        = models.DateTimeField(auto_now=True)
    first_name        = models.CharField(max_length=50)
    last_name         = models.CharField(max_length=50)
    
    is_superuser      = models.BooleanField(default=True)
    is_active	      = models.BooleanField(default=True)
    is_staff	 	  = models.BooleanField(default=True)

    
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    objects = SuperUserAccountManager()
    
    
    
    def __str__(self) -> str:
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_staff
 
    def has_module_perms(self, app_label):
        return True
    
    @property
    def token(self):
        payload = {
            'username': self.username, 'email': self.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        return token


class AdminAccountManager(BaseUserManager):
    
    def create_user(self, username, email, first_name, last_name, company_name, admin_type, password=None):
        user = self.model(
            username     =username,
            email        =self.normalize_email(email),
            first_name   =first_name,
            last_name    =last_name,
            company_name = company_name,
            admin_type   = admin_type,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
class AdminAccount(AbstractBaseUser):
    ADMIN_TYPE = [
        ('main', 'Main'),
        ('inherit', 'Inherit')
    ]
    username     = models.CharField(max_length=50, unique=True)
    email        = models.EmailField(max_length=50, unique=True)
    date_joined  = models.DateTimeField(auto_now_add=True)
    last_login   = models.DateTimeField(auto_now=True)
    first_name   = models.CharField(max_length=50)
    last_name    = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    admin_type   = models.CharField(max_length=50, choices=ADMIN_TYPE, default=ADMIN_TYPE[1][0])
    
    is_active	 = models.BooleanField(default=True)

    
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'company_name', 'type_admin']
    
    objects = AdminAccountManager()
    
    
    
    def __str__(self) -> str:
        return f'{self.username} {self.company_name}'
    
    def has_perm(self, perm, obj=None):
        return None
 
    def has_module_perms(self, app_label):
        return True
    
    @property
    def token(self):
        payload = {
            'username': self.username, 'email': self.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        return token



class InstructorAccountManager(BaseUserManager):
    
    def create_user(self, username, email, first_name, last_name, department, company_name, instructor_type, password=None):
        user = self.model(
            username   =username,
            email      =self.normalize_email(email),
            first_name =first_name,
            last_name  =last_name,
            department = department,
            company_name =company_name,
            instructor_type = instructor_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
class InstructorAccount(AbstractBaseUser):
    INSTRUCTOR_TYPE = [
        ('doctor', 'Doctor'),
        ('assistant', 'Assistant'),
        ('trainer', 'Trainer')
    ]
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=50, unique=True)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    department      = models.CharField(max_length=50)
    company_name    = models.CharField(max_length=50)
    instructor_type = models.CharField(max_length=50, choices=INSTRUCTOR_TYPE, default=INSTRUCTOR_TYPE[0][0])
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)


    is_active	= models.BooleanField(default=True)

    
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'department', 'company_name', 'instructor_type']
    
    objects = InstructorAccountManager()
    
    
    
    def __str__(self) -> str:
        return f'{self.username} {self.instructor_type}'
    
    def has_perm(self, perm, obj=None):
        return None
 
    def has_module_perms(self, app_label):
        return True
    
    @property
    def token(self):
        payload = {
            'username': self.username, 'email': self.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        return token



class StudentAccountManager(BaseUserManager):
    
    def create_user(self, username, email, first_name, last_name, company_name, id_college, department, gender, age, national_id, parent_national_id, password=None):
        user = self.model(
            username           =username,
            email              =self.normalize_email(email),
            first_name         =first_name,
            last_name          =last_name,
            company_name       = company_name,
            id_college         = id_college,
            department         = department,
            gender             = gender,
            age                = age,
            national_id        = national_id,
            parent_national_id = parent_national_id,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
class StudentAccount(AbstractBaseUser):
    GENDER_TYPE = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    username           = models.CharField(max_length=50, unique=True)
    email              = models.EmailField(max_length=50, unique=True)
    date_joined        = models.DateTimeField(auto_now_add=True)
    last_login         = models.DateTimeField(auto_now=True)
    first_name         = models.CharField(max_length=50)
    last_name          = models.CharField(max_length=50)
    company_name       = models.CharField(max_length=70)
    id_college         = models.CharField(max_length=20, null=True, blank=True)
    department         = models.CharField(max_length=50)
    gender             = models.CharField(max_length=10, choices=GENDER_TYPE, default=GENDER_TYPE[1][0])
    age                = models.IntegerField()
    national_id        = models.CharField(max_length=50)
    parent_national_id = models.CharField(max_length=50)

    is_active	      = models.BooleanField(default=True)

    
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'company_name', 'department', 'gender', 'age', 'national_id', 'parent_national_id']
    
    objects = StudentAccountManager()
    
    
    
    def __str__(self) -> str:
        return f'{self.username} {self.company_name}'
    
    def has_perm(self, perm, obj=None):
        return None
 
    def has_module_perms(self, app_label):
        return True
    
    @property
    def token(self):
        payload = {
            'username': self.username, 'email': self.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        return token



class ParentAccountManager(BaseUserManager):
    
    def create_user(self, username, email, first_name, last_name, national_id, password=None):
        user = self.model(
            username     =username,
            email        =self.normalize_email(email),
            first_name   =first_name,
            last_name    =last_name,
            national_id  = national_id,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
class ParentAccount(AbstractBaseUser):
    username          = models.CharField(max_length=50, unique=True)
    email             = models.EmailField(max_length=50, unique=True)
    first_name        = models.CharField(max_length=50)
    last_name         = models.CharField(max_length=50)
    national_id       = models.CharField(max_length=50)
    date_joined       = models.DateTimeField(auto_now_add=True)
    last_login        = models.DateTimeField(auto_now=True)
    
    is_active	      = models.BooleanField(default=True)

    
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'national_id']
    
    objects = ParentAccountManager()
    
    
    
    def __str__(self) -> str:
        return f'{self.username} {self.national_id}'
    
    def has_perm(self, perm, obj=None):
        return None
 
    def has_module_perms(self, app_label):
        return True
    
    @property
    def token(self):
        payload = {
            'username': self.username, 'email': self.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        return token


class CompanyRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    company_name        = models.CharField(max_length=50)
    admins_number       = models.IntegerField()
    instrauctors_number = models.IntegerField()
    students_number     = models.IntegerField()
    start               = models.DateField()
    end                 = models.DateField()
    is_sign_up          = models.BooleanField(default=True)
    contact_email       = models.EmailField()
    description         = models.TextField(max_length=200)
    status               = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    
    
    def __str__(self):
        return f'{self.company_name} : {self.contact_email}'
    
class Company(models.Model):
    company_name        = models.CharField(max_length=50, unique=True)
    admins_number       = models.IntegerField()
    instrauctors_number = models.IntegerField()
    students_number     = models.IntegerField()
    start               = models.DateField()
    end                 = models.DateField()
    is_sign_up          = models.BooleanField(default=True)
    contact_email       = models.EmailField(unique=True)
    description         = models.TextField(max_length=200)
    
    def __str__(self):
        return self.company_name


class ExtraPermissions(models.Model):
    user_have_perm = models.CharField(max_length=50, unique=True)
    company_name = models.CharField(max_length=50)

    add_doctor = models.BooleanField(default=False)
    delete_doctor = models.BooleanField(default=False)
    update_doctor = models.BooleanField(default=False)
    # -----------
    add_assistant = models.BooleanField(default=False)
    delete_assistant = models.BooleanField(default=False)
    update_assistant = models.BooleanField(default=False)
    # ----------
    add_trainer = models.BooleanField(default=False)
    delete_trainer = models.BooleanField(default=False)
    update_trainer = models.BooleanField(default=False)
    # ------------
    add_admin = models.BooleanField(default=False)
    delete_admin = models.BooleanField(default=False)
    update_admin = models.BooleanField(default=False)
    # ------------
    add_student = models.BooleanField(default=False)
    delete_student = models.BooleanField(default=False)
    update_student = models.BooleanField(default=False)
    # ------

    # admin
    add_course = models.BooleanField(default=False)
    add_schedule = models.BooleanField(default=False)
    add_instructor_schedule = models.BooleanField(default=False)
    add_student_schedule = models.BooleanField(default=False)  # admin ins
    delete_instructor_schedule = models.BooleanField(default=False)

    delete_course = models.BooleanField(default=False)  # ins admin delete student from sch
    # --------------- inst-------------- #
    open_course = models.BooleanField(default=False)  # ins
    upload_materials = models.BooleanField(default=False)
    add_quiz = models.BooleanField(default=False)
    add_task = models.BooleanField(default=False)
    #
    add_post = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user_have_perm} : {self.company_name}'