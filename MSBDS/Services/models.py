from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.utils import timezone

# Define User Levels


class AccessLevel(models.Model):
    name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# Define User
class CustomUser(AbstractUser):
    ADMIN_ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agricultural expert', 'Agricultural expert'),
    )

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    
    admin_role = models.CharField(max_length=19, choices=ADMIN_ROLE_CHOICES, default='admin')
    
    def __str__(self):
        return self.username

     # Override the save method to handle password hashing
    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password if the user is being created
            self.set_password(self.password)
        super().save(*args, **kwargs)



class Farmer(models.Model):
    username = models.CharField(max_length=100)
    farmSize=models.IntegerField(default=20)
    farmLocation = models.CharField(max_length=10)
    contact = models.CharField(max_length=20) 
    severity=models.CharField(max_length=100,default='low')

    def __str__(self):
        return str(self.name)













