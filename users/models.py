import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from config.models import BaseModel
from datetime import datetime, timedelta
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken
import random


SUPER_ADMIN, ADMIN, USER = ("super_admin", 'admin', 'user')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')
NEW, CODE_VERIFIED, DONE, PHOTO_DONE = ("new", 'code_verified', 'done', 'photo_done')


class User(AbstractUser, BaseModel):
    USER_ROLES = (
        (SUPER_ADMIN, SUPER_ADMIN),
        (ADMIN, ADMIN),
        (USER, USER)
    )

    AUTH_TYPE_CHOICE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )

    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE)
    )

    user_role = models.CharField(max_length=31, choices=USER_ROLES, default=USER)
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE_CHOICE, default=VIA_EMAIL)
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    email = models.EmailField(null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True, unique=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def create_verify_code(self, verify_type):
        code = "".join([str(random.randint(0,100) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id = self.id,
            verify_type = verify_type,
            code = code)
        return code
    
    def check_username(self):
        if not self.username:
            temp_username = f"user-{uuid.uuid4().__str__().split('-')[-1]}"
            while User.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{random.randint(0,9)}"
            self.username = temp_username

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()
            self.email = normalize_email

    def check_pass(self):
        if not self.password:
            temp_password = f"password-{uuid.uuid4().__str__().split('-')[-1]}"
            self.password = temp_password
    
    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)
    
    
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access" : str(refresh.access_token),
            "refresh": str(refresh)
        }
    
    
    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)


    def clean(self):
        self.check_username()
        self.check_email()
        self.check_pass()
        self.hashing_password()

    


PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5

class UserConfirmation(BaseModel):
    TYPE_CHOICES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES, default=VIA_EMAIL)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_isconfirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())
    

    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expiration_time = datetime.now()+timedelta(minutes=EMAIL_EXPIRE)
        else:
            self.expiration_time = datetime.now()+timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='avatar.jpg', upload_to='users/', validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','heic','heif'])])
    
    def __str__(self):
        return f'{self.user.username} Profile'