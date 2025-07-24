# logistics/urls.py
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from loginapp.views import CustomPasswordResetView

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='signup'),
    path('logout/', views.out, name='logout'),
    path('changepass/', views.changepass, name='changepass'),
    path('resetpass/', views.resetpass, name='resetpass'),
    path('reset-password/', CustomPasswordResetView.as_view(template_name='resetpass.html'), name='password_reset'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='login.html'),name='password_reset_done'),
    # Add more URLs for additional functionalities like logout, dashboard, etc.
]
