from django.db import models


class City(models.Model):

    name = models.CharField(unique=True, max_length=255)
    counter = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name