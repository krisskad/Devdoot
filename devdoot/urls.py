from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.dashboard_page, name='dashboard'),
    path('requestedproblems/', views.requested_problems, name='requestedproblems'),
    path('solvedproblems/', views.solved_problems, name='solvedproblems'),
    path('profile/', views.profilePage, name='profile'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
