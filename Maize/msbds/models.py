from django.db import models

# Create your models here.
class Farmer(models.Model):
    username = models.CharField(max_length=100)
    farmSize=models.IntegerField(default=20)
    farmLocation = models.CharField(max_length=10)
    contact = models.CharField(max_length=20) 
    severity=models.CharField(max_length=100,default='low')

    def __str__(self):
        return str(self.name)