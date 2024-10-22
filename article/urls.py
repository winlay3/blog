from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='home'),
    path('blog/<int:id>', views.article,name="article"),
    path('join/signup', views.signup, name = 'signup'),
    path('join/login', views.login,name='login'),
    path('join/logout',views.logout, name = 'logout'),
    path('manage/blog/create',views.create_article , name="create_article")
]