from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='home'),
    path('join/signup', views.signup, name = 'signup'),
    path('join/login', views.login,name='login'),
    path('join/logout',views.logout, name = 'logout')
]