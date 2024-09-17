from django.urls import path

from companies import views

urlpatterns = [
    path('', views.CompaniesView.as_view(), name='companies'),
]
