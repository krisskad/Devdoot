
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('load-cities/', views.load_cities, name='ajax-load-cities'),
    path('forgot/', views.forgotPage, name='forgot'),
    path('reset_password/', views.resetPage, name='reset_password'),
    path('logout/', views.logoutUser, name="logout"),
]
