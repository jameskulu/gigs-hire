from django.urls import path
from . import views

urlpatterns = [
    path("", views.musician_view),
    path("<int:pk>", views.single_musician_view),
    path("send-enquiry/", views.send_enquiry_musician),
]
