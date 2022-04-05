from django.db import models


class myperson(models.Model):
    name = models.CharField(max_length=16)
