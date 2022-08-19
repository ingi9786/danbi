from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


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

    account    = models.ForeignKey(User, on_delete=models.CASCADE)
    title      = models.CharField(max_length=50)
    category   = models.CharField(max_length=15, choices=Category.choices, default=Category.MIRACLE)
    goal       = models.CharField(max_length=50)
    is_alarm   = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


class RoutineResult(TimeStampedModel):
    class Result(models.TextChoices):
        NOT  = "not", _("안함")
        TRY  = "try", _("시도")
        DONE = "done", _("완료")

    routine    = models.OneToOneField(Routine, on_delete=models.CASCADE)
    result     = models.CharField(max_length=4, choices=Result.choices, default=Result.NOT)
    is_deleted = models.BooleanField(default=False)


class RoutineDay(TimeStampedModel):
    class Day(models.TextChoices):
        MON = "mon", _("월");  TUE = "tue", _("화")
        WED = "wed", _("수");  THU = "thu", _("목")
        FRI = "fri", _("금");  SAT = "sat", _("토");  SUN = "sun", _("일")

    day        = models.CharField(max_length=3, choices=Day.choices)
    routine    = models.ManyToManyField(Routine)
