from django.db import models

class Classification(models.Model):
    name = models.CharField(max_length=100)

