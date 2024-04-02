import uuid
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, UserManager, BaseUserManager
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
# Create your models here.

class UserManager(BaseUserManager):

    use_in_migrations = True
    def _create_user(self,first_name,last_name,email,password,**extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")
        
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,last_name=last_name,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self,first_name=None,last_name=None,email=None,password=None,**extra_fields):
        # extra_fields.setdefault('is_business_owner',False)
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(first_name,last_name,email,password,**extra_fields)

    def create_superuser(self,first_name="Admin",last_name="Admin",email=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(first_name,last_name,email,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 25, blank=True,default='',unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255,blank=True,default='')
    last_name = models.CharField(max_length=255,blank=True,default='')
    # uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    phone_number = models.CharField(validators=[RegexValidator(
                regex=r'^01\d{1}\d{3}\d{4}$',
                message="Phone number must start with '01' and be entered in the format: '01X-XXX XXXX'.",
            )], max_length=12, blank=True,null=False)
    
    avatar = models.ImageField(upload_to='avatar',blank=True,null=True)


    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)  # New field for banning users

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True,null=True)

    objects=UserManager()

    USERNAME_FIELD='email'
    EMAIL_FIELD='email'
    REQUIRED_FIELDS=[]
