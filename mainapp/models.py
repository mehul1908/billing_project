from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

#Table for User (specifically Teacher)
class User(AbstractUser):
	address = models.CharField(max_length=50)
	college_name = models.CharField(max_length=50 ,  default="International Institute of Professional Studies")
	pan_card = models.CharField(max_length=10)
	bank = models.CharField(max_length=20)
	bank_addr = models.CharField(max_length=50)
	bank_ac_no = models.IntegerField(default=0)
	ifsc_code = models.CharField(max_length=11)

	def __str__(self) -> str:
		return self.username

#Table for Course
class Course(models.Model):
	id = models.CharField(max_length=4 , primary_key=True)
	name =  models.CharField(max_length=10)

	def __str__(self) -> str:
		return self.id + self.name
	
#Table for Subject
class Subject(models.Model):
	id =  models.CharField(max_length=7 , primary_key=True)
	name = models.CharField(max_length=20)
	sem = models.IntegerField()
	course = models.ForeignKey(to=Course , on_delete=models.CASCADE)
	user_id = models.ForeignKey(to=User  , on_delete=models.DO_NOTHING , blank=True, null=True)

#Table for Storing the Billing Details
class Billing(models.Model):
	teacher = models.ForeignKey(to=User  , on_delete=models.DO_NOTHING)
	course =  models.ForeignKey(to=Course , on_delete=models.DO_NOTHING)
	subject = models.ForeignKey(to=Subject , on_delete=models.DO_NOTHING)
	date = models.DateTimeField(default=datetime.now)
