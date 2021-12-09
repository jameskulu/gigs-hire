from django.db import models

ROLE_CHOICES = (
    ("user", "user"),
    ("admin", "admin"),
)


class User(models.Model):
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=150, blank=True, null=True)
    lastName = models.CharField(max_length=150, blank=True, null=True)
    password = models.CharField(max_length=150)
    about = models.TextField(max_length=500, blank=True, null=True)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default="user")
    isActive = models.BooleanField(default=True)
    isVerified = models.BooleanField(default=False)
    emailToken = models.CharField(max_length=150, blank=True, null=True)
    emailTokenExpireDate = models.DateTimeField(blank=True, null=True)
    resetToken = models.CharField(max_length=150, blank=True, null=True)
    resetTokenExpireDate = models.DateTimeField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.email
