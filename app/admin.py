from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(department)
admin.site.register(degree)
admin.site.register(student)
admin.site.register(staff)
admin.site.register(subject)
admin.site.register(semester)
admin.site.register(cia)
admin.site.register(CustomUser)
