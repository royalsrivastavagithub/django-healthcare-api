from django.db import models

from accounts.models import User


class Doctor(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    years_of_experience = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
