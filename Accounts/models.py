from django.db import models
from Category.models import Category

GENDER_CHOICES = (
    ("male", "male"),
    ("female", "female"),
    ("others", "others"),
)


class Musician(models.Model):
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=150, blank=True, null=True)
    lastName = models.CharField(max_length=150, blank=True, null=True)
    password = models.CharField(max_length=150)
    about = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.TextField(max_length=500, blank=True, null=True)
    address = models.TextField(max_length=150, blank=True, null=True)
    city = models.TextField(max_length=150, blank=True, null=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, blank=True, null=True
    )
    isActive = models.BooleanField(default=True)
    isVerified = models.BooleanField(default=False)
    emailToken = models.CharField(max_length=150, blank=True, null=True)
    emailTokenExpireDate = models.DateTimeField(blank=True, null=True)
    resetToken = models.CharField(max_length=150, blank=True, null=True)
    resetTokenExpireDate = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
    )
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.email
