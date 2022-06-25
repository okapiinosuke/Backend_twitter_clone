from django.urls import include, path

from . import views

app_name = 'account'


urlpatterns = [
    path('', views.start_view, name='start'),
    path('register/', views.register_view, name='register'),
    path('register/complete/', views.complete_view, name='complete'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
]
