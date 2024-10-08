from django.urls import path

from users import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('', views.UserView.as_view(), name='user'),
]
