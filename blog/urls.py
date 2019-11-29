from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('article/<int:permalink>/', views.article, name='article'),
]
