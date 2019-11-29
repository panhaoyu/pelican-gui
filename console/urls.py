from django.urls import path
from . import views

app_name = 'console'
urlpatterns = [
    path('update/', views.update, name='update'),
    path('edit/<int:permalink_id>/', views.edit, name='edit'),
    path('', views.index, name='index'),
]
