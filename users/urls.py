from django.urls import path
from  . import views

urlpatterns = [
    path('init/', views.AuthView),
    path('redirect/', views.CalendarView),
]