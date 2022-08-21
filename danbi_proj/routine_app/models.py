from django.db import models
# from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.conf import settings


class UsersManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_staffuser(self, email, password):
        user = self.create_user(email,password=password,)
        user.staff = True
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password):
        user = self.create_user(email,password=password,)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class Myuser(AbstractBaseUser):
    email=models.CharField(primary_key=True,max_length=155)
    active=models.BooleanField(default=True)
    staff=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)
    time_stamp=models.TimeField(auto_now_add=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    
    def get_first_name(self):
        return self.email
    def get_short_name(self):
        return self.email
    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    @property
    def is_active(self):
        return self.active
   
    object= UsersManager()
    
    class Meta:
        db_table = "my_user"
    

# Create your models here.
# 이거 나중에 빼놓자. 
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Routine(TimeStampedModel):
    class Category(models.TextChoices):
        MIRACLE  = "miracle", _("기상관련")
        HOMEWORK = "homework", _("숙제관련")

    routine_id = models.BigAutoField(primary_key=True)
    account    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title      = models.CharField(max_length=50)
    category   = models.CharField(max_length=15, choices=Category.choices, default=Category.MIRACLE)
    goal       = models.CharField(max_length=50)
    is_alarm   = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        db_table = "routine"


class RoutineResult(TimeStampedModel):
    class Result(models.TextChoices):
        NOT  = "not", _("안함")
        TRY  = "try", _("시도")
        DONE = "done", _("완료")

    routine_result_id = models.BigAutoField(primary_key=True)
    routine           = models.OneToOneField(Routine, on_delete=models.CASCADE)
    result            = models.CharField(max_length=4, choices=Result.choices, default=Result.NOT)
    is_deleted        = models.BooleanField(default=False)
    
    class Meta:
        db_table = "routine_result"


class RoutineDay(TimeStampedModel):
    class Day(models.TextChoices):
        MON = "mon", _("월");  TUE = "tue", _("화")
        WED = "wed", _("수");  THU = "thu", _("목")
        FRI = "fri", _("금");  SAT = "sat", _("토");  SUN = "sun", _("일")

    day        = models.CharField(max_length=3, choices=Day.choices)
    routine    = models.ManyToManyField(Routine)
    
    class Meta:
        db_table = "routine_day"
