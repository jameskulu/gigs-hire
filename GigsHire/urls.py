from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("Accounts.api.urls")),
    path("categories/", include("Category.api.urls")),
    path("musicians/", include("Musician.api.urls")),
]
