
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name='register'),
    path('load-cities/', views.load_cities, name='ajax-load-cities'),

    url('validate_email/', views.validate_email, name='validate_email'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='login/reset_password.html'),
         name='reset_password'),

    path('reset_password_sent/',
             auth_views.PasswordResetDoneView.as_view(template_name='login/email_sent_message.html'),
             name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
             auth_views.PasswordResetConfirmView.as_view(template_name='login/password_reset_form.html'),
             name='password_reset_confirm'),

    path('reset_password_complete/',
                 auth_views.PasswordResetCompleteView.as_view(template_name='login/password_reset_successfully.html'),
                 name='password_reset_complete'),
]

# password reset builtin method
'''
 1: send reset link on email       //PasswordResetView.as_view()
 2: Email send success message     //PasswordResetDoneView.as_view()
 2: Link to password reset form    //PasswordResetConfirmView.as_view()
 3: Password successfully changed  //PasswordResetCompleteView.as_view()
'''
