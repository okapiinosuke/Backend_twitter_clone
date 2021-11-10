from django.urls import include, path

from . import views

app_name = 'account'

register_patterns = ([
    path('', views.register_view, name='register'),
    path('complete/', views.complete_view, name='complete')
])

urlpatterns = [
    path('', views.start_view, name='start'),
    path('register/', include(register_patterns)),
    path('login/', views.login_view, name='login'),
]
