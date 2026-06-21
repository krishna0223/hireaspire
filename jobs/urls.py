from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_setup, name='profile_setup'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
]
