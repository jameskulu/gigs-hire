from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)
