from django.urls import path
from . import views

app_name = 'console'
urlpatterns = [
    path('', views.index, name='index'),
]
