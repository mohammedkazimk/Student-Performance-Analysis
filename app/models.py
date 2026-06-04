from django.db import models
from .manager import *
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    role = models.CharField(max_length=10,choices=[("student","Student"),("staff","Staff"),("admin","Admin")],default="admin")

    REQUIRED_FIELDS = []
    objects = UserManager()

class department(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class degree(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class student(models.Model):
    name = models.CharField(max_length=50)
    rollno = models.IntegerField(unique=True)
    regno = models.CharField(max_length=30,unique=True)
    dob = models.DateField()
    dept = models.ForeignKey(department,on_delete = models.CASCADE,related_name="depart")
    course = models.ForeignKey(degree,on_delete=models.CASCADE,related_name="deg")
    gender = models.CharField(max_length=7,choices=[('male','Male'),('female','Female')],default='NULL')
    admission = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class staff(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    dept = models.ForeignKey(department,on_delete=models.CASCADE,related_name="dept")
    course = models.ForeignKey(degree,on_delete=models.CASCADE,related_name="degre")
    designation = models.CharField(max_length=80)

    def __str__(self):
        return self.name

class subject(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20)
    semester = models.SmallIntegerField(choices=[(1,'Semester 1'), (2,'Semester 2'), (3,'Semester 3'), (4,'Semester 4'), (5,'Semester 5'), (6,'Semester 6') ])
    credit = models.SmallIntegerField()
    staff = models.ForeignKey(staff,on_delete=models.SET_NULL,null=True,related_name="substaff")
    course = models.ForeignKey(degree,on_delete=models.CASCADE,related_name="subcourse")
    part = models.SmallIntegerField(default=1,choices=[(1,'Part 1'),(2,'Part 2'),(3,'Part 3'),(4,'Part 4'),(5,'Part 5')])

    def __str__(self):
        return self.name

class semester(models.Model):
    sub = models.ForeignKey(subject,on_delete=models.CASCADE,related_name="subject")
    stu = models.ForeignKey(student,on_delete=models.CASCADE,related_name="stud")
    sem = models.SmallIntegerField(choices=[(1,'1 Semester'), (2,'2 Semester'), (3,'3 Semester'), (4,'4 Semester'), (5,'5 Semester'), (6,'6 Semester')])
    internal = models.SmallIntegerField()
    external = models.SmallIntegerField()

    def __str__(self):
        return self.stu.name

class cia(models.Model):
    sub = models.ForeignKey(subject,on_delete=models.CASCADE,related_name="subj")
    stu = models.ForeignKey(student,on_delete=models.CASCADE,related_name="student")
    sem = models.SmallIntegerField(choices=[(1,'1 Semester'), (2,'2 Semester'), (3,'3 Semester'), (4,'4 Semester'), (5,'5 Semester'), (6,'6 Semester')])
    cia = models.SmallIntegerField(choices=[(1,'C.I.A - I'), (2,'C.I.A - I'), (3,'C.I.A - III')])
    mark = models.SmallIntegerField()
    assignment = models.BooleanField()

    def __str__(self):
        return self.stu.name