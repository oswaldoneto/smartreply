from django.db import models


class Classification(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Property(models.Model):
    classification = models.ForeignKey(Classification)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=250)

