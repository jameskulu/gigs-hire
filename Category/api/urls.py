from django.urls import path
from . import views

urlpatterns = [
    path("", views.categories_view),
    path("<int:pk>", views.single_category_view),
]
