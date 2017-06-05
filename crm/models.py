from django.db import models


class Campanha(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.name


