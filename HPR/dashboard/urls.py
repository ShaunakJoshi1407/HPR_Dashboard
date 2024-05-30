from django.urls import path
from . import views

urlpatterns = [
    path('', views.run_script, name='run_script'),
]
