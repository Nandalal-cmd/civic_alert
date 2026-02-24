from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('upvote/<int:complaint_id>/', views.upvote_complaint, name='upvote_complaint'),
    path('admin/login/', views.admin_login_view, name='admin_login'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/update/<int:complaint_id>/', views.admin_update_complaint, name='admin_update_complaint'),
]