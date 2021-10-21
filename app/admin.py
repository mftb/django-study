from django.contrib import admin
from app.models import Course, Grade, Student


myModels = [Course, Grade, Student]  # iterable list
admin.site.register(myModels)
