from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50)
    students = models.ManyToManyField('app.Student')


class Student(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField('app.Course')

    class Meta:
        ordering = ['name']


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
