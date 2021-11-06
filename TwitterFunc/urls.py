from django.urls import path
from . import views


urlpatterns = [
    path('', views.start, name='start'), 
    path('register/', views.register, name='register'), 
    path('register/complete', views.complete, name='complete'), 
    path('login/', views.login, name='login'), 
]
