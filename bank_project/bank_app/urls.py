from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy


urlpatterns = [
    path('', views.home_redirect, name='home'),  # Redirect root to login
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    path('transactions/', views.transaction_history, name='transactions'),
    path('apply-loan/', views.apply_loan, name='apply_loan'),

    # Auth views
    path(
    'login/',
    auth_views.LoginView.as_view(
        template_name='login.html',
        success_url=reverse_lazy('dashboard')
    ),
    name='login'
),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]