from django.contrib import admin
from .models import Myuser, Routine, RoutineDay, RoutineResult

# Register your models here.
admin.site.register(Myuser)
admin.site.register(Routine)
admin.site.register(RoutineDay)
admin.site.register(RoutineResult)
