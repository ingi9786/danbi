from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class UsersManager(BaseUserManager):
    def create_user(self, email, user_name, first_name, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must have an email address!'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True'
            )
        return self.create_user(email, user_name, first_name, password, **other_fields)

class Myuser(AbstractBaseUser):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    about = models.TextField(max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS= ["user_name", "first_name"]
    
    objects = UsersManager()
    
    def __str__(self):
        return self.user_name
    
    def get_full_name(self):
        pass
    def get_short_name(self):
        pass
    @property
    def is_superuser(self):
        return self.is_admin
    @property
    def is_staff(self):
        return self.is_admin
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return self.is_admin
    @is_staff.setter    
    def is_staff(self, value):
        self._is_staff = value


    class Meta:
        db_table = "my_user"
    

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Routine(TimeStampedModel):
    class Category(models.TextChoices):
        MIRACLE  = "miracle", _("????????????")
        HOMEWORK = "homework", _("????????????")

    routine_id = models.BigAutoField(primary_key=True)
    account    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title      = models.CharField(max_length=50)
    category   = models.CharField(max_length=15, choices=Category.choices, default=Category.MIRACLE)
    goal       = models.CharField(max_length=50)
    is_alarm   = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    
    @property
    def days(self):
        return self.routineday_set.all()

    @property
    def result(self):
        return self.routineresult_set.all()

    class Meta:
        db_table = "routine"


class RoutineResult(TimeStampedModel):
    class Result(models.TextChoices):
        NOT  = "not", _("??????")
        TRY  = "try", _("??????")
        DONE = "done", _("??????")

    routine_result_id = models.BigAutoField(primary_key=True)
    routine           = models.ForeignKey(Routine, on_delete=models.CASCADE)
    result            = models.CharField(max_length=4, choices=Result.choices, default=Result.NOT)
    is_deleted        = models.BooleanField(default=False)
    
    class Meta:
        db_table = "routine_result"
        

class RoutineDay(TimeStampedModel):
    class Day(models.TextChoices):
        MON = "mon", _("???");  TUE = "tue", _("???")
        WED = "wed", _("???");  THU = "thu", _("???")
        FRI = "fri", _("???");  SAT = "sat", _("???");  SUN = "sun", _("???")
    
    day        = models.CharField(max_length=3, choices=Day.choices)
    routine    = models.ForeignKey(Routine, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "routine_day"